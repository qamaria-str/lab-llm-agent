# LLM agent for laboratory liquid handling (proof of concept)

A Python agent that uses an LLM (Gemini API, function calling) to turn
natural language instructions (French/English) into actions on a
**simulated** liquid handling robot.

## How it works
1. `robot.py`: simulated liquid handler (tips, aspirate, dispense) that
   refuses invalid commands (volume limits, missing tip, empty well).
2. `agent.py`: the LLM chooses which robot functions to call. Robot errors
   are sent back to the LLM so it can correct its sequence.
3. `eval.py`: runs test instructions and checks the final plate state.

## Run it
    pip install google-genai
    export GEMINI_API_KEY="your-key"
    python agent.py

## Results
- 3/3 valid transfer instructions succeeded (including a multi-well
  distribution).
- Impossible cases (unknown plate, empty well, volume too large): not yet
  evaluated (free API quota reached).

## Limitations
- Simulator only, no real hardware.
- Very small test set; single run per test.
- Plate and well names are not fully validated in the simulator.
- Free-tier API quota limits testing.