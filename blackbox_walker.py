from avulto import DMM, DME, DMI, Path as p, Dir, dmlist
from avulto.ast import Prefab, Attribute, Identifier, Call # type: ignore

class SS13:
  def __init__(self, dmefile):
    self.dme = DME.from_file(dmefile, parse_procs=True)
    self.feedback_keys = dict()

  def visit_Expr(self, node):
    if isinstance(node, Call) and isinstance(node.expr, Identifier):
      if str(node.expr) == "SSblackbox" and node.name == "record_feedback":
        self.feedback_keys[node.args[1]] = node.args[0]

  def walk(self, pth, proc):
    self.feedback_keys = dict()
    self.dme.walk_proc(pth, proc, walker=self)
    print("Found feedback types:")
    print(self.feedback_keys)

ss13 = SS13("D:/ExternalRepos/third_party/Paradise/paradise.dme")
