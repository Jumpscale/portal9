def main(j, args, params, *other_args):
    params.result = page = args.page

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])

    input = j.data.serializer.yaml.loads(content)
    title = input.get('title')
    data = input.get('data')
    legends = input.get('legends')
    page.addPieChart(title=title, data=data, legend=legends)

    return params
