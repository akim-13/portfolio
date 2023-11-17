# Concept

## Multi-Room Disco System

- One arduino used to process and control outputs to the other agent arduinos.

- **Inputs**:
    1. Buttons - Used to pause and play music.
    2. Infrafred/Motion Sensor - Turns off music when motion isn't detected for an extended period (saves energy).
    3. Potentiometer - Turn music up and down on each of the agent arudinos.
    4. Volume Sensor - Safety feature which turns down the volume if a new speaker is too loud. Failsafe to notify the parent arduino if a speaker is broken.

- **Outputs**:
    1. LEDs - Disco lights to BPM of any song.
    2. Speakers - Play music.
    3. LCD - Shows volume in each room. Warns when music is too loud. Announces songs in each room.

- **Justification**:
    Motion & volume detector arduino - When everyone leaves, turn off the music (saves energy).

- **Questions**:
    - How much justification to seperate Arduinos?
    - Can we hook up and SD card to an Arduino to play music?
    - Do they have all the sensorys necessary?

# Plan
- **Week 1** (*Nov 13th to 19th*):
    - **Sunday** — each team should have a detailed spec describing their system's functionality and why we need it by the end of the week. Upload it to your designated markdown file on GitHub (`ME_spec.md` for Morgan and Eddie, `AV_spec.md` for Akim and Vlad).
- **Week 2** (*Nov 20th to 26th*):
    - **Monday** — start working on your systems.
    - **Friday** — meet up at the lab to discuss progress and further plans. Continue working on the systems.
- **Week 3** (*Nov 27th to Dec 3rd*):
    - **Tuesday or Wednesday** — finish working on your system. Each team should have both hardware and software working. *Importantly*, no time should be wasted on optimizing the software or making it look as good as possible, since it'll probably become a mess after merging anyway. However, obviously, it has to make sense and be somewhat readable and understandable. 
    - **Wednesday or Thursday** — meet up and merge hardware (3 Arduinos) together. It's important to do this before the Friday lab, since we'll probably have questions when we start merging code and figuring out how it should all work together.
    - **Friday** — meet up at the lab to start merging code.
- **Week 4** (*Dec 3rd to 10th*):
    - **Wednesday** — finish merging code and have the entire system working. We might need to meet up before Wednesday in case there are some issues that cannot be resolved remotely.
    - **Thursday** — start working on the report and video.
    - **Sunday** — finish everything and upload on Moodle.
- **Week 5** (*Dec 11th*):
    - **MONDAY 8PM DEADLINE** — go through the submitted material just in case, and resolve any potential issues (god forbid).
