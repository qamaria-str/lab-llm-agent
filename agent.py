from google import genai
from google.genai import types
from robot import LiquidHandler

MODEL = "gemini-3.1-flash-lite"
client = genai.Client(http_options=types.HttpOptions(timeout="360000"))

robot = LiquidHandler()


# ---------- Les outils que le LLM peut demander d'appeler ----------
# Les descriptions (docstrings) sont lues par le LLM : elles lui
# expliquent à quoi sert chaque fonction.

def pick_up_tip() -> str:
    """Fixe une pointe de pipette neuve sur le robot."""
    return robot.pick_up_tip()


def drop_tip() -> str:
    """Jette la pointe actuelle."""
    return robot.drop_tip()


def aspirate(plate: str, well: str, volume_ul: float) -> str:
    """Aspire un volume (en microlitres) depuis un puits.
    plate : 'plate_1' ou 'plate_2'. well : ex. 'A1'."""
    return robot.aspirate(plate, well, volume_ul)


def dispense(plate: str, well: str, volume_ul: float) -> str:
    """Dispense un volume (en microlitres) dans un puits.
    plate : 'plate_1' ou 'plate_2'. well : ex. 'B1'."""
    return robot.dispense(plate, well, volume_ul)


TOOLS = {f.__name__: f for f in (pick_up_tip, drop_tip, aspirate, dispense)}

SYSTEM_PROMPT = (
    "Tu pilotes un robot de pipetage. Utilise uniquement les fonctions "
    "fournies pour exécuter les instructions de l'utilisateur. "
    "Si une fonction renvoie une erreur, corrige ta séquence d'actions. "
    "Quand tout est fait, résume ce que tu as fait en une phrase."
)

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    tools=list(TOOLS.values()),
    # On exécute nous-mêmes les fonctions, pour garder le contrôle
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)


def run_instruction(instruction: str, max_steps: int = 20) -> None:
    contents = [types.Content(role="user", parts=[types.Part(text=instruction)])]

    for _ in range(max_steps):
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config
        )
        calls = response.function_calls

        if not calls:  # pas d'appel demandé : le LLM a fini
            print("LLM :", response.text)
            return

        # On garde la réponse du LLM dans l'historique
        contents.append(response.candidates[0].content)

        results = []
        for call in calls:
            print(f"  → {call.name}({dict(call.args)})")
            try:
                output = {"result": TOOLS[call.name](**call.args)}
            except ValueError as e:
                output = {"error": str(e)}
                print(f"  ✗ refusé par le robot : {e}")
            results.append(
                types.Part.from_function_response(name=call.name, response=output)
            )
        # On renvoie les résultats au LLM
        contents.append(types.Content(role="user", parts=results))

    print("Arrêt : trop d'étapes sans conclusion.")


if __name__ == "__main__":
    run_instruction("Transfère 50 µL de plate_1 A1 vers plate_2 B1.")
    print("État des plaques :", robot.wells)