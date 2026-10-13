# Printer Cabinet

Parametric workshop printer cabinet designed with CadQuery and built with 3/4" Baltic birch plywood.

## Project Overview

This repository contains the CAD design for a dedicated, multi-tier workshop printer cabinet engineered to house both 3D printing and 2D printing/scanning workflows:

- **Dimensions**: Approximately 6' high (72" / 1828.8 mm), 2' wide (24" / 609.6 mm), and 2' deep (24" / 609.6 mm).
- **Primary Material**: 3/4" (19.05 mm) Baltic birch plywood for the carcass, structural shelves, and door frames; 1/2" (12.7 mm) Baltic birch for the inset shear back panel, tool drawer box, and tray lips.
- **Multi-Stage Vibration Isolation & Ballast**:
  - *Bottom Ballast Paver*: A dense 18" x 18" concrete/granite paver slab (~22 kg) housed inside the base plinth beneath the paper shelf, anchoring the center of mass right at floor level.
  - *Printer Inertia Platform*: A second 18" x 18" concrete paver slab (~22 kg) resting on a 1/2" (12 mm) high-density closed-cell EVA / Sorbothane damping pad directly beneath the Prusa Core One+, cutting printhead jerk displacement in half.
  - *Double-Laminated 1.5" Shelf*: Two face-glued 3/4" Baltic birch panels (38.1 mm total) with a 1.5" front stiffener apron rib to eliminate shelf deflection and acoustic drumming.
  - *Acoustic Wall Tether*: A heavy-duty steel angle bracket with a neoprene rubber isolation grommet mounted at the upper rear to lock the 6' cabinet to a wall stud against sway while decoupling motor vibrations.
  - *Base Decoupling Feet*: Four industrial rubber machine leveling feet isolating the plinth from floor joists.
- **3D Printer Enclosure & Exhaust System**:
  - Enclosed with a framed Baltic birch door and 1/8" clear acrylic viewing window.
  - 120 mm enclosure exhaust fan and 4" (100 mm) round duct collar flange to vent fumes/VOCs directly out to a room window.
- **Top Filament Dry Chamber**: Upper storage compartment with a sealed gasketed acrylic door, desiccant bead trays, dual-roller spool rack, and PTFE pass-through tubes to feed directly into the printer below.
- **Shallow Tool Drawer**: Positioned directly under the 3D printer shelf on 22" full-extension slides; sized for modular Gridfinity bins, spare nozzles, scrapers, calipers, and maintenance tools.
- **Pull-Out Inkjet/Scanner Shelf**: Located below the tool drawer on 22" heavy-duty slides; extends forward so the Epson flatbed scanner lid opens 100% unobstructed.
- **Lower Paper Storage**: Compact bottom bay for up to 6 reams of paper (3,000 sheets) and 11x17 boxes.

## Development & AI Policy: The "Centaur" Approach

This project is developed using a collaborative human-AI workflow. The code, architecture, and documentation were written and refined with the assistance of advanced AI models. 

I approach AI not as a tool for blind self-automation, but as a collaborative interaction. I aspire to be a [centaur](https://mitsloan.mit.edu/ideas-made-to-matter/3-ways-to-use-ai-are-you-a-cyborg-a-centaur-or-a-self-automator), "... maintain[ing] structured and controlled interactions with AI, harnessing it as a tool for targeted efficiency". I acknowledge that when learning a new domain I might be a cyborg "... collaborat[ing] closely with the AI tool -- probing its suggestions, allowing it to lead the way, and taking its advice on some occasions while pushing back against it on others." Both are OK. In this model, the AI acts as a high-powered pair-programming partner. It helps me rapidly explore and develop my own understanding of complex topics. Meanwhile, I hold the strategic vision, conduct the physical testing/validation, and apply and build domain knowledge as I go.

For rules regarding AI-assisted contributions from the community, please see the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project utilizes a **Dual License** structure to comply with both software and open-source hardware best practices. These specific open-source licenses were chosen to support the transition to an anarchist economy—promoting mutual aid, free distribution of information, and breaking down artificial scarcity.

*   **Software (Python Code):** All source code in this repository is licensed under the [GNU General Public License v3.0 (GPLv3)](COPYING). This ensures that any modifications to the code remain open-source and provides explicit patent protections.
*   **Hardware (3D Models):** The generated output files (STL and STEP files) are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](LICENSE). This is the standard license for the 3D printing community.
