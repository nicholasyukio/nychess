def evaluate_value(item):
    # Your function to evaluate the value for each element
    return len(item)

# Your original list
original_list = ["apple", "banana", "avocado", "kiwi", "pineapple", "strawberry", "pear", "orange"]

# Sort the list based on the evaluated value
sorted_list = sorted(original_list, key=evaluate_value, reverse=True)

# Select only the N elements with the highest value
N = 3  # Change this to the desired number of elements
selected_elements = sorted_list[:N]

print(selected_elements)
