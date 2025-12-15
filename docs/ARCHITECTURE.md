# Runtime view diagrams and how to regenerate

This small `docs/` folder contains two PlantUML diagrams that provide a meaningful runtime view of the project:

- `runtime_sequence.puml` — a sequence diagram showing the runtime interactions when the program processes one image / frame.
- `runtime_component.puml` — a high-level component (runtime) view showing components, responsibilities, and main interactions.

Why PlantUML?
- PlantUML is easy to read and edit by hand. It produces sequence and component diagrams useful for architecture docs.
- You can preview the `.puml` files with a VS Code PlantUML extension or render them offline with `plantuml.jar`.

How to render (quick):

1) Using VS Code
  - Install the 'PlantUML' extension (or 'PlantUML extension by jebbs').
  - Open any `*.puml` file and use the preview (Alt+D or the PlantUML preview commands).

2) Using the plantuml.jar (requires Java)
  - Download `plantuml.jar` from https://plantuml.com/download
  - From the repo root run (PowerShell):

```powershell
# render both diagrams
java -jar path\to\plantuml.jar docs\runtime_sequence.puml
java -jar path\to\plantuml.jar docs\runtime_component.puml

# output PNGs will appear next to the .puml files
```

3) Use online preview services
  - Copy/paste the `.puml` text into the PlantUML online server/editor or VS Code plugin.

Notes and tips
- If you want a machine-derived runtime trace (actual call timings / flamegraphs), use a tracer like `viztracer` or `pyinstrument` to produce a dynamic trace, then manually convert the interesting call sequence to a PlantUML sequence diagram.
- The sequence diagram in this folder is intentionally compact and focused on the main components: `main.py`, `LoadSources`, `ImageProcessor`, `DataLogger`, and `GeometricObjectsGui`.
- If you'd like, I can also produce a PNG of these diagrams and add them to the repo (requires Graphviz/PlantUML runtime or Java). Tell me whether you want me to render and commit PNGs.

Suggested next steps
- If you want an exact runtime trace taken from your code, pick one: I can run `viztracer` over a single-image run and produce an interactive HTML trace.
- If you want a richer C4-style diagram, I can draft a C4 container/context view in PlantUML or Structurizr DSL.
