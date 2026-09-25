# Candidate release discipline

Keep protocol 0.1-rc.4-candidate, MCP 0.2.0rc1 and Skill 0.2.0-rc.1 until the release prerequisites are met. Candidate distribution for bounded use is allowed; it must remain visibly labeled candidate. No new final rc.4 tag, DOI or promotion is created by these scripts.

1. Verify historical hashes/tags; preserve rc.3 PDFs, workbook and archive.
2. Regenerate candidate schema/docs/Skill copies and run the complete regression suite, real MCP transport and isolated Skill tests. Retain actual results and source hashes.
3. Review public/private attribution and download contents. Keep raw correspondence and pilot identifiers outside public source/packages unless separately permitted.
4. Verify candidate PDFs and website links/rendering; distinguish all rc.3 archive links.
5. Record at least one bounded actual external end-user/advisor use, with permission, exact versions, evidence digests, elapsed time, gate outcomes and feedback. A stop may be valuable; success is not required.
6. Author reviews current test evidence and the reality/permission of the pilot records, unresolved issues and limitations. Only then consider a separately versioned final rc.4 promotion. One pilot does not establish controlled effectiveness.

Current actual-use registry is empty. Correspondence and synthetic fixtures do not satisfy step 5. scripts/verify_candidate.py records REMAIN_CANDIDATE until the prerequisite exists; it never publishes or promotes automatically.
