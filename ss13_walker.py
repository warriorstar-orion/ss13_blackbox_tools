from avulto import DMM, DME, DMI, Path as p, Dir, dmlist
from avulto.ast import Prefab, Attribute, Identifier
import random


class SS13:
	def __init__(self, dmefile):
		self.dme = DME.from_file(dmefile, parse_procs=True)
		self.global_lists = dict()
		self.random_spawners = dict()

	def visit_Expr(self, node):
		if not self.found:
			self.assignment = node.rhs
			self.found = True

	def global_list(self, name):
		if name not in self.global_lists:
			self.found = False
			self.assignment = None
			self.dme.walk_proc("/datum/controller/global_vars", f"InitGlobal{name}", self)
			if self.found:
				self.global_lists[name] = self.assignment
				return self.assignment
		return self.global_lists[name]
	
	def random_spawner(self, pth):
		if pth not in self.random_spawners:
			self.random_spawners[pth] = self.dme.typedecl(pth)
		return self.random_spawners[pth]
	
	def super_recursive_pick(self, list_to_pick):
		result = pick_weight_recursive(list_to_pick)

		if isinstance(result, Prefab) and result.path.child_of("/obj/effect/spawner/random"):
			result_loot = self.random_spawner(result.path).value("loot")
			return self.super_recursive_pick(result_loot)
		elif isinstance(result, Attribute):
			if isinstance(result.expr, Identifier) and str(result.expr) == "GLOB":
				sublist = self.global_list(result.name)
				return self.super_recursive_pick(sublist)

		return result

def fill_with_ones(list_to_pad):
	if not isinstance(list_to_pad, dmlist):
		return list_to_pad

	final_list = dict()

	for key in list_to_pad.keys():
		if list_to_pad[key]:
			final_list[key] = list_to_pad[key]
		else:
			final_list[key] = 1

	return final_list


def pickweight(L):
	total = 0
	item = None
	for item, val in L.items():
		total += val

	total = random.uniform(0, total)
	for item, val in L.items():
		total -= val
		if total <= 0:
			return item

	return None


def pick_weight_recursive(list_to_pick):
	result = pickweight(fill_with_ones(list_to_pick))
	while isinstance(result, dmlist):
		result = pickweight(fill_with_ones(result))
	return result

def prob(P):
    r = random.randint(1, 100)
    if r <= P:
        return 1
    return 0

