import sys

base_description = {
    "Expression": {
        "Chain": [["Expression", "left"], ["Expression, right"]],
        "Unary": [["scanner.Token", "operator"], ["Expression", "right"]],
        "Binary": [["Expression", "left"], ["scanner.Token", "operator"], ["Expression", "right"]],
        "Grouping": [["Expression", "expression"]],
        "Literal": [["object", "value"]]
    },
    "Statement": {
        "Expression": ["Expr expression"],
        "Print" : ["Expr expression"]
    }
}

def defineAST(output_file, base_name: str, types: dict):
    """
    Creates classes for Abstract Syntax Tree
    """
    output_file.write("import scanner\n\n")
    output_file.writelines(["class " + base_name + ":\n",
                            "\tpass\n"])
    for expr_type, expr in types.items():
        defineType(output_file, base_name, expr_type, expr)

def defineType(output_file, base_name, class_name, fields):
    """
    Creates classes for AST sub-trees
    """
    names = [field[-1] for field in fields]

    field_str = ", ".join(names)

    var_defs = ["\t\tself." + name + " = " + name + "\n" for name in names]

    output_file.write("\n")
    output_file.writelines(["class " + class_name + "(" + base_name + "):\n"
                            "\tdef __init__(self, " + field_str + "):\n"])
    output_file.writelines(var_defs)
    output_file.write("\n")
    output_file.writelines(["\tdef accept(self, visitor):\n", 
                            "\t\treturn visitor.visit" + class_name + "(self)\n"])

if __name__ == "__main__":
    path = "grammar.py"
    with open(path, "w+") as file:
        defineAST(file, "Expression", base_description["Expression"])

    # Class attributes in statement.py are listed as "self.n"
    # I fixed this manually and renamed to self.expression to keep moving forward
    path = "statement.py"
    with open(path, "w+") as file:
        defineAST(file, "Stmt", base_description["Statement"])