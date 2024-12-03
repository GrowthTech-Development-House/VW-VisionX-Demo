

def countedBOM(items):
    output = []
    for item in items:
        if item in output:
            pass
        output[item] += 1

    print(f'Output: {output}')
    return output
