def files_list():
    """Creates the files lists that display the files used to create each section
    of the page.
    """
    vars = request.vars
    title = request.args[0]
    position = request.args[1]

    files_list = []
    for item in vars:
      files_list.append(LI(item + ": ", (A(vars[item][0], _href=
          URL('show_code', 'read', vars=dict(file=vars[item]), extension='html')))))

    return dict(title=title, files_list=files_list, position=position)
