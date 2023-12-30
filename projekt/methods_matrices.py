import json
from projekt.models import Scales, DecisionScenarios, Models, Criterias, Alternatives
from projekt.models import Experts, Matrices, DataWeights, MatriceElements, ScenarioWeights, DataElements


def make_decision_tree(decisionScenario: DecisionScenarios) -> list:
    tree = []
    model = Models.objects.get(pk=decisionScenario.modelID.pk)
    criterias = Criterias.objects.filter(modelcriterias__modelID=model)
    rootCriterion = criterias.get(parent_criterion__isnull=True)
    rootChildren = criterias.filter(parent_criterion=rootCriterion)
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

    return tree
        

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

def calculate_weights(decisionScenario: DecisionScenarios):
    tree = make_decision_tree(decisionScenario)
    for criterium, size in tree:
        criteria = Criterias.objects.get(pk=criterium)
        if not DataWeights.objects.filter(criteriaID=criteria).exists():
            dataweight, _ = DataWeights.objects.update_or_create(criteriaID=criteria, size=size)
            ScenarioWeights.objects.update_or_create(weightsID=decisionScenario, dataWeights=dataweight)
        else:
            dataweight = DataWeights.objects.get(criteriaID=criteria, size=size)
            ScenarioWeights.objects.update_or_create(weightsID=decisionScenario, dataWeights=dataweight)

        matrices = Matrices.objects.filter(criteriaID=criteria)
        matriceelements = [[MatriceElements.objects.filter(matrixID=matrice), matrice.size] for matrice in matrices]
        matrixes = [[[queryset[0][i+queryset[1]*j].value for i in range(queryset[1])] for j in range(queryset[1])] for queryset in matriceelements]
        products = []
        for matrix in matrixes:
            products.append(geometric_mean_matrix(matrix))
        result = geometric_mean_N_vectors(products)
        for index, value in enumerate(result):
            DataElements.objects.update_or_create(dataWeightsID=dataweight, x=index, value=value)


def get_values(decisionScenario: DecisionScenarios):
    model = Models.objects.get(pk=decisionScenario.modelID.pk)
    alternatives = Alternatives.objects.filter(modelalternatives__modelID = model)
    
    criterias = Criterias.objects.filter(modelcriterias__modelID=model)
    rootCriterion = criterias.get(parent_criterion__isnull=True)
    # tmp = DataWeights.objects.filter(criteriaID=rootCriterion)
    # print(DataElements.objects.filter(dataWeightsID__in=tmp))
    values = [0 for _ in range(len(alternatives))]
    def recursive(criterium):
        childreen = Criterias.objects.filter(parent_criterion = criterium)
        print(childreen)
        print('weszlem')
        # print(childreen[0])
        print('siemanoko')
        if (Criterias.objects.filter(parent_criterion = criterium).exists()):
            childs = childreen.values_list()
            weights = [recursive(item) for item in childs]
            tmp = DataWeights.objects.filter(criteriaID=criterium)
            criterium_weights= DataElements.objects.filter(dataWeightsID__in=tmp)
            print(criterium_weights)
            criterium_weights_list = criterium_weights.values_list()
            criterium_weights_list = [item[3] for item in criterium_weights_list]
            dzielnik = sum(criterium_weights_list)
            print(f'criterium weights list: {criterium_weights_list}')
            print(weights)
            print(f'dlugosc dzieci: {len(childs)}')
            val = [0 for _ in range(len(alternatives))]
            for i in range(len(alternatives)):
                for j in range(len(childs)):
                    val[i] += weights[j][i] * criterium_weights_list[j] / dzielnik
            return val
        tmp = DataWeights.objects.filter(criteriaID=criterium)
        alternatives_weights = DataElements.objects.filter(dataWeightsID__in=tmp)
        alternatives_weights_list = alternatives_weights.values_list()
        print(f'tutaj liść: {alternatives_weights_list}')
        val = [item[3] for item in alternatives_weights_list]
        dzielnik = sum(val)
        for i in range(len(val)):
            val[i] /= dzielnik
        print(f'zformatowany lisc {val}')
        return val
    v = recursive(rootCriterion)
    # suma = sum(v)
    # for i in range(len(v)):
    #     v[i]/=suma
    return v

    

def generate_json_file(decisionScenario: DecisionScenarios):
    model = Models.objects.get(pk=decisionScenario.modelID.pk)
    alternatives = Alternatives.objects.filter(modelalternatives__modelID=model)
    criterias = Criterias.objects.filter(modelcriterias__modelID=model)
    experts = Experts.objects.filter(modelexperts__modelID=model)
    scales = Scales.objects.filter(modelscales__modelID=model)
    print(scales)
    matrices = Matrices.objects.filter(datamatrices__dataID=decisionScenario.dataID)
    weightsy = DataWeights.objects.filter(scenarioweights__weightsID=decisionScenario.weightID)
    data = {}
    data["decision_scenario_id"] = decisionScenario.pk
    data["model_id"] = model.pk
    data["data_id"] = decisionScenario.dataID
    data["weights_id"] = decisionScenario.weightID
    data["model"] = {}
    data["model"]["alternatives"] = [{"id": alternative.pk, "name": alternative.name, "description": alternative.description} for alternative in alternatives]
    data["model"]["criteria"] = [{"id": criteria.pk, "parent_criterion": criteria.parent_criterion.pk if isinstance(criteria.parent_criterion, int) else None,
                                   "name": criteria.name, "description": criteria.description} for criteria in criterias]
    data["model"]["experts"] = [{"id": expert.pk, "name": expert.name, "address": expert.address} for expert in experts]
    data["model"]["ranking_method"] = model.ranking_method
    data["model"]["aggregation_method"] = model.aggregation_method
    data["model"]["completeness_required"] = model.completeness_required
    data["model"]["scale"]  = [{"value": scale.value, "description": scale.description} for scale in scales]

    matriceelements = [[MatriceElements.objects.filter(matrixID=matrice), matrice.size] for matrice in matrices]
    matrixes = [[[queryset[0][i+queryset[1]*j].value for i in range(queryset[1])] for j in range(queryset[1])] for queryset in matriceelements]
    data["data"] = [{"id": matrice.pk, "criteria_id": matrice.criteriaID.pk, "expert_id": matrice.expertID.pk, "pcm": matrixes[index]} for index, matrice in enumerate(matrices)]
    
    weightselements = [[DataElements.objects.filter(dataWeightsID=weight), weight.size] for weight in weightsy]
    weights = [[queryset[0][i].value for i in range(queryset[1])] for queryset in weightselements]
    data["weights"] = [{"criterion_id": weight.criteriaID.pk, "w": weights[index]} for index, weight in enumerate(weightsy)]

    return data
