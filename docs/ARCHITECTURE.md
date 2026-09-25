# THEDU Phase 1 Architecture

## Goal
THEDU is a local, relevance-first lexical search engine.

```text
Query
  ↓
Normalization
  ↓
Tokenization
  ↓
Inverted Index
  ↓
BM25 Ranking
  ↓
Snippet Generation
  ↓
Results
 
Layers
text

API / CLI
   ↓
Services
   ↓
Core Search Components + Storage + Ingestion