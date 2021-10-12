import matplotlib.pyplot as plt
plt.style.use('ggplot')

input_message = "Enter a missed question-type or .q to quit \n"
err = input(input_message).capitalize()
error_dict = {}

while err.lower() != ".q":
    if err in error_dict:
        error_dict[err] += 1
    else:
        error_dict[err] = 1
    err = input(input_message).capitalize()

err_types = list(error_dict.keys())
err_count = [error_dict[err_type] for err_type in error_dict]

fig = plt.figure(figsize=(12, 8))

x_pos = [i for i, _ in enumerate(err_types)]

plt.bar(x_pos, err_count, color='blue')
plt.xlabel("Passage")
plt.ylabel("Error Frequency")
plt.title("Errors")

plt.xticks(x_pos, err_types)

plt.show()
