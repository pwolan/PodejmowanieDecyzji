import json
from projekt.models import Scales, DecisionScenarios, Models, Criterias, Alternatives, Experts, Matrices

# TODO Usunąć? Jeśli można
def add_scale(): # TYLKO PRZY RESTARCIE BAZY DANYCH
    Scales.objects.create(value=0.25, description="4 razy gorsze")
    Scales.objects.create(value=1/3, description="3 razy gorsze")
    Scales.objects.create(value=0.5, description="2 razy gorsze")
    Scales.objects.create(value=1, description="Porównywalne")
    Scales.objects.create(value=2, description="2 razy lepsze")
    Scales.objects.create(value=3, description="3 razy lepsze")
    Scales.objects.create(value=4, description="4 razy lepsze")

def make_decision_tree(decisionScenario: DecisionScenarios) -> list:
    tree = []
    model = Models.objects.get(pk=decisionScenario.modelID.pk)
    criterias = Criterias.objects.filter(modelcriterias__modelID=model)
    rootCriterion = criterias.get(parent_criterion__isnull=True)
    rootChildren = criterias.filter(parent_criterion=rootCriterion)
    print(rootChildren)
    tree.append([rootCriterion.pk, len(rootChildren)])
    while len(tree) < len(criterias):
        first_instance = rootChildren[0]
        rootChildren = rootChildren[1:]
        instance_ids = [obj.id for obj in rootChildren]
        rootChildren = Criterias.objects.filter(id__in=instance_ids)
        first_instance_children = Criterias.objects.filter(parent_criterion=first_instance)
        if len(first_instance_children) == 0:
            alternatywki = Alternatives.objects.filter(modelalternatives__modelID=model)
            tree.append([first_instance.pk, len(alternatywki)])
        else:
            tree.append([first_instance.pk, len(first_instance_children)])
        rootChildren = rootChildren | first_instance_children
    print(tree)

    return tree
        
        # combined_queryset = initial_queryset | YourModel.objects.filter(id=additional_instance.id)

def geometric_mean(vector: list[int|float]):
    if len(vector) == 0:
        return -1
    product = 1

    for num in vector:
        product *= num

    geometric_mean = product**(1/len(vector))
    return geometric_mean

def geometric_mean_matrix(matrix: list[list[int|float]]):
    if len(matrix) == 0 or len(matrix[0]) == 0:
        return -1
    product = [1 for _ in range(len(matrix))]
    
    for i in range(len(matrix)):
        product[i] = geometric_mean(matrix[i])

    #geometric_mean_matrix = [product[i]**(1/len(matrix[i])) for i in range(len(matrix))]
    return product

def geometric_mean_N_vectors(vectors: list[list[int|float]]):
    if len(vectors) == 0 or len(vectors[0]) == 0:
        return -1
    product = [1 for _ in range(len(vectors[0]))]

    for i in range(len(vectors[0])):
        for j in range(len(vectors)):
            product[i] *= vectors[j][i]

    result = [product[i]**(1/len(vectors)) for i in range(len(vectors[0]))]
    return result

def generate_json_file(decisionScenario: DecisionScenarios):
    model = Models.objects.get(pk=decisionScenario.modelID.pk)
    alternatives = Alternatives.objects.filter(modelalternatives__modelID=model)
    criterias = Criterias.objects.filter(modelcriterias__modelID=model)
    experts = Experts.objects.filter(modelexperts__modelID=model)
    scales = Scales.objects.filter(modelscales__modelID=model)
    matrices = Matrices.objects.filter(datamatrices__dataID=decisionScenario.dataID)
    data = {}
    data["decision_scenario_id"] = decisionScenario.pk
    data["model_id"] = model.pk
    data["model"] = {}
    print(data)
    data["model"]["alternatives"] = [{"id": alternative.pk, "name": alternative.name, "description": alternative.description} for alternative in alternatives]
    data["model"]["criteria"] = [{"id": criteria.pk, "parent_criterion": criteria.parent_criterion.pk, "name": criteria.name, "description": criteria.description} for criteria in criterias]
    print(data)
    data["model"]["experts"] = [{"id": expert.pk, "name": expert.name, "address": expert.address} for expert in experts]
    data["model"]["ranking_method"] = model.ranking_method
    data["model"]["aggregation_method"] = model.aggregation_method
    data["model"]["completeness_required"] = model.completeness_required
    data["model"]["scale"]  = [{"value": scale.value, "description": scale.description} for scale in scales]
    
    data["data"] = [{"id": ""} for matrice in matrices]
    data["weights"] = {}
    print(data)
    name = "decisionScenario_" + str(decisionScenario.pk) + ".json"
    with open("name", "w") as json_file:
        json.dump(data, json_file, indent=2)
#TESTY
# print(geometric_mean([]))
# print(geometric_mean([1]))
# print(geometric_mean([1,2]))
# print(geometric_mean([0.1,0.1,3,4,5]))

# print(geometric_mean_matrix([[1,2,4,5,2],
#                              [2,1,2,3,2],
#                              [4,2,1,5,5],
#                              [5,3,5,1,4],
#                              [2,2,5,4,1]]))

# print(geometric_mean_N_vectors([[1,2,4,5,2],
#                                 [2,1,2,3,2],
#                                 [4,2,1,5,5],
#                                 [5,3,5,1,4],
#                                 [2,2,5,4,1]]))