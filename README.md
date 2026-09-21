# MedFindr

**Version: X1.0 (Defined Version)**  
**Status:** Solid developmental base – Defined milestone

MedFindr is a structured and explainable health-concern assistant created as a focused med × pharma portfolio project.  
It takes a free-text health concern and returns a clear, sectioned, transparent response suitable for patients or pharmacy/clinic staff.

This X1.0 release marks a defined, stable foundation. The architecture is clean, extensible, and ready for further practical development.

---

### Core Capabilities (X1.0)

- Structured Response Engine
- Transparent rule-based urgency & red-flag assessment
- Explainable risk layer (EBM interface + training pipeline)
- Patient / Staff dual view
- Evaluation script against labelled set
- OpenFDA drug lookup with safety-relevant fields
- Clean separation of concerns

### Quick Start

```bash
git clone https://github.com/sablepushkar/MedFindr.git
cd MedFindr
pip install -r requirements.txt
streamlit run app.py
```

### Recommended Setup

```bash
# Train the Explainable Boosting Machine (optional but recommended)
python scripts/train_ebm.py

# Run evaluation
python scripts/evaluate.py
```

### Important Notice

**This is not medical advice.**  
MedFindr is a developmental research and portfolio prototype only.  
It must not be used for actual clinical decisions. Always consult a qualified healthcare professional.

---

### Project Structure

```
MedFindr/
├── app.py                      # Thin UI layer (Patient / Staff view)
├── config.py                   # Central configuration
├── scripts/
│   ├── train_ebm.py            # Train EBM model
│   └── evaluate.py             # Evaluate urgency engine
├── utils/
│   ├── response_engine.py      # Structured response builder
│   ├── urgency.py              # Rule-based urgency engine
│   ├── ebm_risk.py             # Explainable risk module
│   └── drug_lookup.py          # OpenFDA utility
├── data/
│   ├── sample_concerns.json
│   └── evaluation_set.json
├── models/                     # Populated after training
├── requirements.txt
└── README.md
```

---

### Design Principles

- Keep the interface simple and stable
- Keep clinical logic isolated and transparent
- Prefer glass-box / explainable methods
- Make future extensions low-friction

---

### Version Journey

- **09.0** – Stable foundation
- **V09.1a** – Real EBM training pipeline
- **V09 Evolve** – Evaluation + Dual View
- **V1.0 RD** – Redefined and Rechecked
- **X1.0** – Defined Version (current)

---

**MedFindr X1.0** is the official defined developmental base.  
Further practical improvements (richer EBM, drug interactions, live demo, etc.) can be built cleanly on top of this structure.

Built as a focused med × pharma portfolio project.
