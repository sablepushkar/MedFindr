# MedFindr

**Version: V09.1a**  
**Status:** Developmental – Real EBM training pipeline added

MedFindr is a structured, explainable health-concern assistant (med × pharma portfolio project).

---

### Current Capabilities (V09.1a)

- Structured response engine
- Transparent rule-based urgency assessment
- **New:** Real Explainable Boosting Machine training pipeline
- Automatic fallback to transparent placeholder if no model is trained yet
- OpenFDA drug lookup
- Clean architecture

### How to run

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Train the EBM model (recommended)

```bash
python scripts/train_ebm.py
```

This creates `models/ebm_urgency_model.pkl`. The app will automatically use it on next run.

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
│   └── train_ebm.py          # Train the EBM model
├── utils/
│   ├── response_engine.py
│   ├── urgency.py
│   ├── ebm_risk.py
│   └── drug_lookup.py
├── data/
├── models/                   # Created after training
├── requirements.txt
└── README.md
```

---

### Version History

- **09.0** – Stable foundation
- **V09.1a** – Real EBM preparation & training setup

---

Built as a focused med × pharma portfolio project.
