from classes import Company, Employee, Hourly, Commissioned, PointCard, Payagenda, Action
import datetime as dt


def sindicato_func(empresa):
    while True:
        n = input("1 - Definir taxa sindical geral\n2 - Definir taxa sindical adicional\n0 - Retornar\n\n"
                      "undo(u) | redo(r)\n")

        if n == "0":
            empresa.cleanStacks()
            return

        elif n == "1":
            print(f"Taxa atual: {empresa.syndicate.taxes}")
            taxa_geral = float(input("Informe o valor que deseja adicionar para a taxa geral: "))
            action = Action(empresa.actions, None, "generaltaxes", empresa.syndicate.taxes)
            empresa.syndicate.changeGeneralTaxes(taxa_geral)
            print(empresa.syndicate.taxes)

        elif n == "2":
            identificador = input("Informe o identificador do funcionário: ")
            taxa_ad = float(input("Informe a taxa adicional de serviço: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e:
                action = Action(empresa.actions, e, "aditionaltaxes", taxa_ad)
                empresa.syndicate.plusAditionalTaxes(empresa, identificador, taxa_ad)

        elif n == "u":
            empresa.actions.undoRedo(empresa, False)

        elif n == "r":
            empresa.actions.undoRedo(empresa, True)


def adicionar_func(empresa):
    aux1 = ["C", "S", "H"]
    aux2 = ["y", "n"]
    nome = input("Nome: ")
    endereco = input("Endereco: ")
    tipo = input("Tipo de funcionário (C - Comissionado; S - Assalariado; H - Horista): ")
    metodopagamento = input("Método de pagamento: ")
    tipo.upper()
    while tipo not in aux1:
        print("Valor inválido para o atributo!")
        tipo = input("Tipo de funcionário (C - Comissionado; S - Assalariado; H - Horista): ")
        tipo.upper()
    sindicado = str(input("Afiliação sindical (y, n): "))
    sindicado.lower()
    while sindicado not in aux2:
        print("Valor inválido para o atributo!")
        sindicado = str(input("Afiliação sindical (y, n): "))
        sindicado.lower()
    e1 = None

    if(tipo == "H"):
        salario_h = float(input("Salario por hora: "))
        e1 = Hourly(empresa, nome, endereco, tipo, 0, sindicado, salario_h, metodopagamento)
    elif(tipo == "C"):
        salario = float(input("Salario mensal: "))
        comissao = float(input("Taxa de comissão (valor decimal):"))
        e1 = Commissioned(empresa, nome, endereco, tipo, salary=salario, issyndicate=sindicado,
                          comission_percent=comissao, paymethod=metodopagamento)
    elif(tipo == "S"):
        salario = float(input("Salario mensal: "))
        e1 = Employee(empresa, nome, endereco, tipo, salario, sindicado, 0, 0, paymethod=metodopagamento)
    else:
        print("erro")

    return e1


def venda(empresa):
    while True:
        n = input("1 - Registrar uma nova venda\n2 - Ver total de vendas\n0 - Retornar\n\nundo(u) | redo(r)\n")
        if n == "0":
            empresa.cleanStacks()
            return
        elif n == "1":
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e and e.jobtype == "C":
                data = input("informe a data da venda: ")
                valor = float(input("informe o valor da venda: "))
                action = Action(empresa.actions, e, "sale", [data, valor])
                e.addSale(data, valor)
                print("Resultado de venda lançado!")
        elif n == "2":
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e and e.jobtype == "C":
                print(f"Comissão total: {e.comission_amount}")
                print("Vendas efetuadas:")
                for i in e.sales:
                    print (i.value)
        elif n == "u":
            empresa.actions.undoRedo(empresa, False)

        elif n == "r":
            empresa.actions.undoRedo(empresa, True)


def cartao(empresa):
    while True:
        n = input("1 - Adicionar cartão de ponto\n2 - Bater ponto\n0 - Retornar\n\nundo(u) | redo(r)\n")

        if n == "0":
            empresa.cleanStacks()
            return

        elif n == "1":
            print("Essa operação adiciona um cartão de ponto a um funcionário com uma afiliação que não seja horista.")
            print("Informe o ID do funcionário para continuar ou 0 para cancelar a operação")
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            while not e:
                identificador = str(input("Informe um novo ID ou digite 0 para cancelar a operação: "))
                e = Employee.getEmployeeByID(empresa, identificador)
                if identificador == "0":
                    print("Operação cancelada")
                    e = None
                    break

            if e:
                if e.jobtype == "H":
                    print("Funcionários horistas já possuem um cartão associado!")
                else:
                    y = input("Se você prosseguir com a operação, o tipo do funcionário será atualizado para Horista."
                              "Deseja prosseguir? (s/n)\n")
                    if y == "s":
                        aindex = empresa.getPayagendaIndex(e)
                        print("Para concluir a migração é necessário que informe alguns valores:")
                        salary_h = float(input("Digite o seu salário horário: "))
                        e.remove(empresa, e.id)
                        new = Hourly(empresa, e.name, e.address, "H", 0, e.issyndicate, salary_h,
                                     paymethod=e.payment.paymethod, id=e.id)
                        print("Novo cartão de ponto criado!")
                        action = Action(empresa.actions, new, "updatetype", [e, aindex])

        elif n == "2":
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            while not e:
                print("ID inválido")
                identificador = str(input("ID do funcionário: "))
                e = Employee.getEmployeeByID(empresa, identificador)

            e = Employee.getEmployeeByID(empresa, identificador)
            h = int(input("1 - Início de expediente\n2 - Final de expediente\n"))
            if e and h == 1:
                inicio = int(input("Hora de início: "))
                e.punchTheClockIn(inicio)
                action = Action(empresa.actions, e, "clockin", value=inicio)
            elif e and h == 2:
                final = int(input("Hora de encerramento: "))
                e.punchTheClockOut(final, e.workstarthour)
                action = Action(empresa.actions, e, "clockout", value=[e.workstarthour, final])

        elif n == "u":
            empresa.actions.undoRedo(empresa, False)

        elif n == "r":
            empresa.actions.undoRedo(empresa, True)


def funcionario(empresa):
    while True:
        n = (input("1 - Adicionar um novo funcionário\n2 - Remover um funcionário registrado\n3 - Dados do "
                   "funcionário\n4 - Alterar informações de um funcionário\n5 - Alterar afiliação do funcionário\n"
                   "6 - Escolher nova Agenda de Pagamento\n7 -  Mostrar todos os funcionários\n"
                   "0 - Retornar\n\nundo(u) | redo(r)\n"))

        if n == "0":
            empresa.cleanStacks()
            return

        elif n == "1":
            new = adicionar_func(empresa)
            action = Action(empresa.actions, new, "create")
            print("Novo funcionario criado!")
            print(f"ID: {new.id}")

        elif n == "2":
            identificador = str(input("ID do funcionário: "))
            confirme = input("Realmente deseja remover esse funcionario? (y/n)")
            e = Employee.getEmployeeByID(empresa, identificador)
            action = Action(empresa.actions, e, "remove")
            if confirme == "y" and e:
                Employee.remove(empresa, identificador)
                print("Funcionario removido do sistema")
            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")

        elif n == "3":
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            if e:
                e.info()
            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")

        elif n == "4":
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            copy = e
            if e:
                aux = ["name", "salary", "syndicate", "address", "jobtype", "paymethod"]
                print("Digite o atributo que você deseja modificar:")
                a = int(input("|1 - name; 2 - stand salary; 3 - syndicate association; 4 - address;\n|5 - jobtype;"
                              "6 - pay method; 7 - hourly salary; 8 - comission percent\n"))
                old = e.getAttribute(aux[a-1])
                valor = input("Digite o novo valor para o atributo especificado: ")
                new_action = Action(empresa.actions, copy, "update", value=old, attribute=aux[a-1])
                e.update(aux[a-1], valor)

            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")

        elif n == "5":
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            aux3 = {"H": "Horista", "S": "Assalariado", "C": "Comissionado"}
            if e:
                print(f"O tipo atual do funcionário é: {aux3[e.jobtype]}")
                x = input("Realmente deseja alterar o tipo de afiliação trabalhista do funcionário? (s/n)\n")
                if x == "s":
                    aux3.pop(e.jobtype)
                    print(f"Informe o novo tipo que deseja para o funcionário {e.id} ou o valor zero para cancelar a"
                          f"operação:")
                    for i in aux3.keys():
                        print(f"({i}):{aux3[i]}")
                    x = input("")
                    while x not in aux3.keys():
                        if x == "0":
                            break
                        print("Tipo inválido!")
                        x = input("Informe um tipo válido para continuar ou 0 para cancelar a operação: ")
                    new = None
                    aindex = empresa.getPayagendaIndex(e)
                    if x == "0":
                        break

                    elif x == "C":
                        print("Para concluir a migração é necessário que informe alguns valores:")
                        salary = float(input("Digite o seu novo salário: "))
                        comission = float(input("Digite sua taxa de comissão em decimais: "))
                        e.remove(empresa, e.id)
                        new = Commissioned(empresa, e.name, e.address, x, id= e.id, salary=salary,
                                           issyndicate=e.issyndicate, comission_percent=comission,
                                           paymethod=e.payment.paymethod)

                    elif x == "H":
                        print("Para concluir a migração é necessário que informe alguns valores:")
                        salary_h = float(input("Digite o seu salário horário: "))
                        e.remove(empresa, e.id)
                        new = Hourly(empresa, e.name, e.address, x, 0, e.issyndicate, salary_h,
                                     paymethod = e.payment.paymethod, id=e.id)

                    elif x == "S":
                        print("Para concluir a migração é necessário que informe alguns valores:")
                        salary = float(input("Digite o seu novo salário: "))
                        e.remove(empresa, e.id)
                        new = Employee(empresa, e.name, e.address, x, salary, e.issyndicate, 0, 0,
                                      paymethod=e.payment.paymethod, id=e.id)
                    action = Action(empresa.actions, new, "updatetype", [e, aindex])
                    print("Afiliação do funcionário atualizada!")

        elif n == "6":
            identificador = str(input("ID do funcionário: "))
            e = Employee.getEmployeeByID(empresa, identificador)
            aux1 = ["y", "n"]
            set = False
            if e:
                agenda = empresa.returnPayagenda(e)
                if agenda.type == "M":
                    aux = {"beggining": "dia 1", "middle": "dia 15", "end": "último dia útil"}
                    aux2 = ["beggining", "middle", "end"]
                    print("------Agenda atual------")
                    print("Agenda de pagamento mensal")
                    print(f"Pagamentos realizados no {aux[agenda.period]} de cada mês.")
                    confirme = input("Deseja alterar o período de pagamento? (y, n)\n")
                    confirme.lower()
                    if confirme == "y":
                        period = int(input("Digite o número do novo período que gostaria de ser pago:\n"
                                       "1 - Início do mês\n2 - Meio do mês\n3 - Fim do mês\n"))
                        if aux2[period - 1] == aux[agenda.period]:
                            print("Você já está sendo pago nesse período!")

                        else:
                            for a in empresa.payagendas:
                                if a.type == "M" and a.period == aux2[period - 1]:
                                    agenda.employees.remove(e)
                                    a.employees.append(e)
                                    set = True
                            if not set:
                                agenda.employees.remove(e)
                                new = Payagenda()
                                new.assumePayagenda("M", None, aux2[period - 1])
                                new.employees.append(e)
                                empresa.payagendas.append(new)
                            print("Sua agenda de pagamento foi atualizada!")

                else:
                    days = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"]
                    print("------Agenda atual------")
                    tipo = "semanal"
                    if agenda.type == "B":
                        tipo = "bissemanal"
                    print(f"Agenda de pagamento {tipo}")
                    print(f"Pagamentos realizados na {days[agenda.day]}")
                    confirme = input("Deseja alterar o dia de pagamento? (y, n)\n")
                    confirme.lower()
                    if confirme == "y":
                        day = int(input("Digite o novo dia que gostaria de ser pago:\n"
                                           "1 - segunda\n2 - terça\n3 - quarta\n4 - quinta\n5 - sexta\n"))
                        if agenda.day == day - 1:
                            print("Você já está sendo pago nesse dia!")
                        else:
                            for a in empresa.payagendas:
                                if a.type == agenda.type and a.day == day-1:
                                    agenda.employees.remove(e)
                                    a.employees.append(e)
                                    set = True
                            if not set:
                                agenda.employees.remove(e)
                                new = Payagenda()
                                new.assumePayagenda(agenda.type, day - 1, None)
                                new.employees.append(e)
                                empresa.payagendas.append(new)
                            print("Sua agenda de pagamento foi atualizada!")

            else:
                print("ID inválido. Cerfique-se que o funcionário está no sistema.")

        elif n == "7":
            for employee in empresa.employees:
                print(f"Nome: {employee.name} | ID: {employee.id} | Afiliação: {employee.jobtype}")

        elif n == "u":
            empresa.actions.undoRedo(empresa, False)

        elif n == "r":
            empresa.actions.undoRedo(empresa, True)


def pagamentos(empresa):
    d = dt.date.today()

    n = int(input("1 - Fazer pagamentos para o dia de hoje\n2 - Fazer pagamentos para os próximos dias\n"
                  "3 - Criar uma nova agenda de pagamento\n0 - Retornar\n"))
    if n == 0:
        return
    elif n == 1:
        empresa.makePayments([d.day, d.month, d.year], empresa.syndicate.taxes)
    elif n == 2:
        m = int(input(f"Defina a quantidade de dias a partir de hoje {d.day}/{d.month}/{d.year} ao qual deseja efetuar "
                      f"o pagamento: "))
        for i in range(0, m):
            empresa.makePayments([d.day, d.month, d.year], empresa.syndicate.taxes)
            d += dt.timedelta(1)
            i += 30
    elif n == 3:
        aux = ["B", "W", "M"]
        set = False
        type = (input("Que tipo de agenda de pagamento você deseja criar?\nB - Bisemanal\nW - Semanal\nM - Mensal\n"))
        if type not in aux:
            print("Tipo inválido.")
        else:
            aux2 = ["beggining", "middle", "end"]
            new = Payagenda()
            if type == "M":
                period = int(input("Informe o período do mês em que deseja ser pago:\n1 - Início do mês (dia 1)\n"
                                   "2 - Meio do mês (dia 15)\n3 - Final do mês (último dia útil)\n"))
                new.assumePayagenda(type, None, aux2[period-1])
                for agenda in empresa.payagendas:
                    if new.period == agenda.period:
                        print("Agenda já cadastrada!")
                        break
                        set = True
                if not set:
                    empresa.payagendas.append(new)
                    print("A nova agenda foi cadastrada!")

            else:
                day = int(input("Digite o dia da semana que o pagamento ocorrerá:\n"
                                "1 - segunda\n2 - terça\n3 - quarta\n4 - quinta\n5 - sexta\n"))
                new.assumePayagenda(type, day - 1, None)

                for agenda in empresa.payagendas:
                    if new.day == agenda.day and new.type == agenda.type:
                        print("Agenda já cadastrada!")
                        set = True
                if not set:
                    empresa.payagendas.append(new)
                    print("A nova agenda foi cadastrada!")


def main(empresa):
    while True:
        n = int(input("1 - Funcionario\n2 - Cartão de ponto\n3 - Resultado de venda\n4 - Sindicato\n5 - Pagamentos"
                      "\n0 - Sair\n"))
        if n == 0:
            break
        elif n == 1:
            funcionario(empresa)
        elif n == 2:
            cartao(empresa)
        elif n == 3:
            venda(empresa)
        elif n == 4:
            sindicato_func(empresa)
        elif n == 5:
            pagamentos(empresa)


c = Company()
em1 = Hourly(c, "Rafa", "AB", "H", 0, "y", 10, paymethod="cheque")
em2 = Commissioned(c, "Rick", "MCZ", "C", 100, "n", 0.5, paymethod="cartão")
em3 = Employee(c, "Jão", "CA", "S", 100, "y", 0, 0, paymethod= "boleto")

main(c)
