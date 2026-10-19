# Source, authenticity and redistribution
- Author: Kevin Hillstrom, MineThatData.
- Original challenge: https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html
- Original CSV: http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv
- Corroborating catalog: https://www.tensorflow.org/datasets/catalog/hillstrom
- Actual retrieval: original HTTP CSV, not a third-party reserialization or synthetic replacement.
- Retrieval timestamp, byte length and SHA-256: `reports/provenance.json`.
- Verified SHA-256: `0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece`.
- Observed size: 3,964,977 bytes; 64,000 data rows; 12 original columns.

The HTTPS variant initially returned HTTP 503. The author's exact HTTP link returned the complete CSV. The checksum is a locally measured reproducibility pin, not an author-signed authenticity certificate. HTTP lacks transport authenticity; the source URL, source description, row count and schema corroborate this acquisition. Future downloads must match these bytes; changed files fail closed.

The author explicitly invites public analysis in the challenge, but no explicit dataset redistribution license was found in the inspected original post or the TFDS catalog. A documentation-page or software license is not a dataset license. Therefore raw CSV, normalized customer-level CSV and SQLite files are excluded from Git. Users download from the author through the pinned downloader. Only derived aggregate results and code are committed; dashboard downloads are aggregates/diagnostics only. Redistribution permission remains unconfirmed. Obtain explicit permission before adding customer-level bytes to a public repository.

No fallback data was used. TFDS was inspected as a potential alternative, but its conversion was unnecessary once the original link worked. If the original becomes unavailable, restore a previously verified local copy with its provenance manifest, or investigate a documented distribution and reconcile content before changing the pin. Never silently substitute data.

Raw files are never rewritten by the pipeline. A cached file is checksum verified on each run. Original values remain in the normalized dataset; derived columns are added separately. Exact repeated observations remain because the available attributes do not identify unique people.
