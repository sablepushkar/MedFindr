# MedFindr – Developers Notes

Formal record of major updates and decisions.

---

### X1.0 – Defined Version
- Locked the project as a stable developmental base.
- Clean architecture with clear separation between UI and logic.
- Transparent urgency engine, EBM interface, dual view, and evaluation script in place.

### V1.0 RD – Redefined and Rechecked
- Full consistency pass across modules.
- Documentation and versioning cleaned.
- Safety messaging strengthened.

### V09 Evolve
- Added Patient / Staff dual view.
- Introduced evaluation script against the labelled set.

### V09.1a
- Added real EBM training pipeline (`scripts/train_ebm.py`).
- Updated risk module to load a trained model when available.
- Kept safe placeholder as fallback.

### 09.0 and earlier
- Built core foundation: structured response engine, urgency rules, drug lookup, sample data, and evaluation set.
- Focus remained on clean structure and transparency.

---

### Design Decisions
- Prefer glass-box methods over black-box models.
- Keep the UI thin so clinical logic stays testable.
- All major behaviour should remain explainable.
- Future additions (richer models, interactions, etc.) should plug in without rewriting the core.

### Current Limitations
- EBM still benefits from more real-world training data.
- Drug interaction checking is not yet implemented.
- No live demo deployment at this stage.
- Evaluation currently focuses mainly on the rule-based urgency engine.

---

Notes will be updated with every meaningful change.
