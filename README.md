# MedFindr

**Version: V09 Evolve**  
**Status:** Developmental – Evaluation + Dual View added

MedFindr is a structured, explainable health-concern assistant built as a focused med × pharma portfolio project.

---

### Current Capabilities (V09 Evolve)

- Structured response engine
- Transparent rule-based urgency assessment
- Explainable risk layer (EBM-ready + training pipeline)
- **New:** Simple Patient / Staff dual view
- **New:** Evaluation script against the labelled set
- OpenFDA drug lookup
- Clean, extensible architecture

### How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Train the EBM (optional but recommended)

```bash
python scripts/train_ebm.py
```

### Run evaluation

```bash
python scripts/evaluate.py
```

### Important Notice

**This is not medical advice.**  
MedFindr is a developmental prototype only. Always consult a qualified healthcare professional.

---

### Project Structure

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
├── requirements.txt
└── README.md
```

---

### Version History

- **09.0** – Stable foundation
- **V09.1a** – Real EBM training pipeline
- **V09 Evolve** – Evaluation script + Dual View

---

Built as a focused med × pharma portfolio project.
