# MedFindr – Developers Notes

Formal record of major updates and engineering decisions.

---

### X1.0 – Defined Version
- Locked the project as a stable developmental base.
- Clean architecture around urgency assessment, structured responses, EBM preparation, and OpenFDA drug lookup.
- Added a labelled evaluation set and a reproducible evaluation script.

### X1.0+ – Practical upgrades
- Improved EBM feature extraction and training setup.
- Strengthened evaluation and documentation.
- Kept the project intentionally small enough to inspect and extend.

### V2 development – Foundation
- Created a separate V2 development branch from the verified 470031a baseline.
- Added automated regression tests for the existing urgency engine.
- Expanded the evaluation script with a confusion matrix and per-class precision/recall.
- No existing X1.0 clinical-rule behaviour was intentionally changed in this foundation commit.
- V2 changes will be introduced in small, independently reviewable stages.

### Engineering principle
MedFindr is a portfolio prototype, not a clinical decision system. Any future model, drug-safety, or workflow feature must remain auditable, clearly scoped, and backed by an explicit data source rather than fabricated medical knowledge.
