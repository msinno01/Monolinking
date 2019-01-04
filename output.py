class Output:
    def __init__(self, models, out_option):
        self.models = models

        if not out_option:
            self.print_results()
        else:
            self.write_results(out_option)

    def print_results(self):
        print("Model\tScore")
        for model, score in self.models:
            print("{0}\t{1}".format(model,score))

    def write_results(self,out_option):
        if not out_option.endswith(".txt"):
            out_option = "{0}.txt".format(out_option)

        with open(out_option,'w+') as f:
            f.write("Model\tScore\n")
            for model, score in self.models:
                f.write("{0}\t{1}\m".format(model,score))
            f.close()
            
        print("Written to {0}".format(out_option))
