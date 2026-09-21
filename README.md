# MedFindr

**Version: X1.0** (with practical upgrades)

MedFindr is a structured health-concern assistant I built as a focused med × pharma portfolio project.  
It takes a free-text description of a health issue and returns a clear, sectioned response that can be useful for both patients and pharmacy/clinic staff.

The goal was to keep everything transparent, clean, and easy to extend later.

---

### What it currently does

- Breaks a health concern into structured sections
- Runs a transparent rule-based urgency / red-flag check
- Has an explainable risk layer (EBM) – you can train a real model with one command
- Supports simple Patient / Staff dual view
- Looks up basic drug information via OpenFDA
- Comes with an evaluation script so you can measure the urgency engine

### How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Train the EBM model (recommended)

```bash
python scripts/train_ebm.py
```

After training, just restart the app and it will use the real model automatically.

### Run evaluation

```bash
python scripts/evaluate.py
```

### Important

This is **not medical advice**. It is a developmental portfolio prototype only.  
Always consult a proper healthcare professional for real health concerns.

---

### Project structure

```
MedFindr/
├── app.py
├── config.py
├── scripts/
│   ├── train_ebm.py
│   └── evaluate.py
├── utils/
│   ├── response_engine.py
│   ├── urgency.py
│   ├── ebm_risk.py
│   └── drug_lookup.py
├── data/
├── models/
├── DEVELOPERS_NOTES.md
├── requirements.txt
└── README.md
```

---

I kept the architecture simple on purpose so that adding better models, drug interaction checks, or a live demo later stays straightforward.

More details on the development history are in `DEVELOPERS_NOTES.md`.
