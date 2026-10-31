# Graph Summary — delivery-workflow-completion
_Auto-generated from GRAPH_REPORT.md · do not edit manually_
_Regen: `graphify update .`_

## Summary
- 741 nodes · 999 edges · 64 communities (59 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output


## Graph Freshness
- Built from commit: `1ec1279f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).


## God Nodes (most connected - your core abstractions)
1. `register_doc()` - 22 edges
2. `run()` - 22 edges
3. `find()` - 19 edges
4. `write_job()` - 18 edges
5. `call()` - 18 edges
6. `catalog()` - 17 edges
7. `add_entry()` - 16 edges
8. `Thai Accounting Office` - 16 edges
9. `ledger_entries()` - 15 edges
10. `index_scan()` - 15 edges


## Cross-Cutting Nodes (span the most distinct areas of the codebase)
A high-degree node isn't always architecturally central - a widely-used
utility/config file can rack up more edges than a real coupler while only
ever touching one area. This ranks by how many DIFFERENT communities a
node's neighbors span, not by raw edge count.
1. `Base` - bridges 3 areas (14 edges)
2. `call()` - bridges 2 areas (18 edges)
3. `register_doc()` - bridges 1 areas (22 edges)
4. `run()` - bridges 1 areas (22 edges)
5. `find()` - bridges 1 areas (19 edges)
6. `write_job()` - bridges 1 areas (18 edges)
7. `catalog()` - bridges 1 areas (17 edges)
8. `add_entry()` - bridges 1 areas (16 edges)
9. `ledger_entries()` - bridges 1 areas (15 edges)

## Surprising Connections (you probably didn't know these)
- `parties_aka()` --calls--> `parties()`  [EXTRACTED]
  tests/test_graph.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `check()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `init()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `register_doc()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `write_job()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py


_Full map → GRAPH_REPORT.md · query: `graphify query "..."`_
