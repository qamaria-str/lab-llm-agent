import time
import agent

# (instruction, état attendu des plaques à la fin)
TESTS = [
    ("Transfère 50 µL de plate_1 A1 vers plate_2 B1.",
     {"plate_1": {"A1": 950}, "plate_2": {"B1": 50}}),
    ("Mets 20 µL de plate_1 A1 dans chacun des puits B1 à B3 de plate_2.",
     {"plate_1": {"A1": 940}, "plate_2": {"B1": 20, "B2": 20, "B3": 20}}),
    ("Transfer 100 µL from plate_1 A1 to plate_2 C4.",
     {"plate_1": {"A1": 900}, "plate_2": {"C4": 100}}),
    # Cas impossibles : le bon comportement est de ne rien changer
    ("Transfère 50 µL de plate_1 A1 vers plate_3 B1.",
     {"plate_1": {"A1": 1000}, "plate_2": {}}),
    ("Transfère 50 µL de plate_2 C1 vers plate_1 D1.",
     {"plate_1": {"A1": 1000}, "plate_2": {}}),
    ("Transfère 2000 µL de plate_1 A1 vers plate_2 B1.",
     {"plate_1": {"A1": 1000}, "plate_2": {}}),
]


def clean(wells):
    """Retire les puits vides pour comparer simplement."""
    return {p: {w: v for w, v in d.items() if v > 0} for p, d in wells.items()}


success = 0
for i, (instruction, expected) in enumerate(TESTS, 1):
    print(f"\n=== Test {i} : {instruction}")
    agent.robot.__init__()  # remet le robot à zéro
    try:
        agent.run_instruction(instruction)
        ok = clean(agent.robot.wells) == clean(expected)
    except Exception as e:
        print("  Erreur API :", str(e)[:100])
        ok = False
    print("  RÉSULTAT :", "OK" if ok else "ÉCHEC", "| état :", clean(agent.robot.wells))
    success += ok
    time.sleep(3)  # évite de dépasser le quota gratuit

print(f"\nTaux de réussite : {success}/{len(TESTS)}")