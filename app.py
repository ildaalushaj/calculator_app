from flask import Flask, render_template, request
import redis
database = redis.Redis(host="redis", port=6379)
Calculator_App = Flask(__name__)  # Creating our Flask Instance


@Calculator_App.route('/', methods=['GET'])
def index():
    """ Displays the index page accessible at '/' """

    return render_template('index.html')


@Calculator_App.route('/operation_result/', methods=['POST'])
def operation_result():
    """Route where we send calculator form input"""


    error = None
    result = None

    # request.form looks for:
    # html tags with matching "name= "
    first_input = request.form['Input1']
    second_input = request.form['Input2']
    operation = request.form['operation']

    try:

        input1 = float(first_input)
        input2 = float(second_input)


        database.set("msg:input1", str(input1))
        database.set("msg:input2", str(input2))
        database.set("msg:operation", str(operation))
        #database.set("msg:result", str(result))
        msg = database.get("msg:input1")
        msg = database.get("msg:input2")
        msg = database.get("msg:operation")
        #msg = database.get("msg:result")

        print(msg)

        if operation == "+":
            result = input1 + input2

        elif operation == "-":
            result = input1 - input2

        elif operation == "/":
            result = input1 / input2

        elif operation == "*":
            result = input1 * input2

        else:
            operation = "%"
            result = input1 % input2

        return render_template(
            'index.html',
            input1=input1,
            input2=input2,
            operation=operation,
            result=result,
            calculation_success=True
        )

    except ZeroDivisionError:
        return render_template(
            'index.html',
            input1=input1,
            input2=input2,
            operation=operation,
            result="Bad Input",
            calculation_success=False,
            error="You cannot divide by zero"
        )

    except ValueError:
        return render_template(
            'index.html',
            input1=first_input,
            input2=second_input,
            operation=operation,
            result="Bad Input",
            calculation_success=False,
            error="Cannot perform numeric operations with provided input"
        )


if __name__ == '__main__':
    Calculator_App.debug = True
    Calculator_App.run(host='0.0.0.0')
