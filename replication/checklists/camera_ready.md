# Camera-ready artifact release checklist

- [ ] No `.env`, API keys, tokens, credentials, local logs, or private corpora are included.
- [ ] No `rag/index.faiss` or `rag/docs.npy` generated files are included in the archive.
- [ ] `.DS_Store`, editor metadata, and local absolute paths are removed.
- [ ] Author and paper metadata are present in `README.md` and `CITATION.cff`.
- [ ] Funding acknowledgment names FAPEMIG projects `CIN II APQ-06513-25` and `CEX-BIS-00192-25`.
- [ ] The README distinguishes implemented functionality from planned Validation/QA and Knowledge Management.
- [ ] The sanitized seed corpus is present and any additional documents are redistributable.
- [ ] `python replication/scripts/check_artifact.py` passes.
- [ ] `python replication/scripts/smoke_test_retrieval.py` passes in a prepared Python environment.
- [ ] The final public repository/archive URL is recorded in the camera-ready paper or proceedings metadata, if required by the venue.
- [ ] Add the final proceedings DOI/citation after publication when available.
