# MedFindr — development notes

These notes record what I changed and what I still need to check. They are not meant to suggest that the project is finished.

## Recent work: evaluation and source handling

I kept the existing Streamlit app and rule engine rather than replacing the project with a new framework. The latest work was mostly about making failures easier to notice.

- The evaluation scripts check that each case has an ID, concern text and a known expected status.
- Duplicate IDs and malformed cases are rejected before metrics are calculated.
- The signal evaluation can write a JSON report with the fixture hash, source revision, status counts and mismatches.
- Drug lookup tests cover a normal response, a missing result, a timeout, invalid JSON and an unexpected response shape.
- Evidence records distinguish a rule created by MedFindr from information returned by an external source.
- The review form still works in the Streamlit session; it is not saved to a permanent review database.

## Commands I use to check it

~~~bash
python -m unittest discover -s tests -v
python scripts/evaluate.py
python scripts/evaluate_signals.py
python scripts/evaluate_reviews.py
~~~

## Things to remember

The evaluation set is small and manually labelled. A high agreement number only means the current rules matched those examples; it is not a measure of clinical accuracy. The phrase matching is basic and can miss context. OpenFDA can also be unavailable or return a different record than expected, so the app needs to show lookup failures clearly.

## Next useful work

I would rather add a few carefully chosen tricky examples and review the mistakes than add another model or a bigger dashboard. I also need to keep testing the app itself, not only the helper functions.
