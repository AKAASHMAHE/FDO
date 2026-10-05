from rdflib import Graph, RDF, OWL


def main():
    graph = Graph()
    graph.parse("ontology/FDO.owl", format="xml")

    classes = list(graph.subjects(RDF.type, OWL.Class))
    object_properties = list(
        graph.subjects(RDF.type, OWL.ObjectProperty)
    )
    datatype_properties = list(
        graph.subjects(RDF.type, OWL.DatatypeProperty)
    )

    print("OWL triples:", len(graph))
    print("Classes:", len(classes))
    print("Object properties:", len(object_properties))
    print("Datatype properties:", len(datatype_properties))


if __name__ == "__main__":
    main()