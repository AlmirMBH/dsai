import math
import numpy as np
import matplotlib.pyplot as plt


print("a", "b", sep=", ", end="\n")

# Formatting
pi = 3.14159
print(f"My number is {pi:.2f}")

# List (mutable collection of objects)
print("LIST")
numbers = [1, 2, 3, 4]
# list.append(5)
# list.remove(4)
numbers.pop(0) # Delete list element by index and return it
del numbers[1] # # Delete list element by index
print(numbers)

print("MATHS")
result = math.sin(math.pi / 6) + math.tan(math.pi * (math.e ** math.pi))
print(f"tan(π) * e^π: {result}")

print("PRIMES")
def is_prime(num):
    for x in range(2, num):
        if (num%2) == 0:
            return False
    return True

nums = range(1,1000)
primes = list(filter(is_prime, nums))
print(primes)

print("MATRIX TRANSPOSE")
M = np.array([
    ["1", "2", "3"],
    ["1/3.6", "5", "23"],
    ["2^10.5", "42", "cos(80.841)"]
])
print(M.T)

print("2D Graphics")
n = np.arange(1, 101)
x = np.sin(n)
y = np.cos(n)
plt.figure(figsize=(10, 6))
plt.plot(n, x, label='x = sin(n)', color='blue', linestyle='-')
plt.plot(n, y, label='y = cos(n)', color='red', linestyle='--')
plt.xlabel('n')
plt.ylabel('Function Values')
plt.title('Plot of x = sin(n) and y = cos(n)')
plt.legend()
plt.grid()
plt.show()

print("3D Scatter")
x = np.random.randn(100)
y = np.random.randn(100)
plt.figure(figsize=(10, 6))
plt.scatter(x[x > 0], y[x > 0], color='blue', label='x > 0')
plt.scatter(x[x <= 0], y[x <= 0], color='red', label='x ≤ 0')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Scatter Plot of Random Points with Normal Distribution')
plt.legend()

print("MATRIX")
matrix = np.ones((2, 2)) # 2x2 with ones as elements
print(matrix)

matrix = np.zeros((4, 3)) # 4x3 with ones as zeros
print(matrix)

M = np.array([
    [1, 2, 3],
    [1, 6, 5],
    [2, 10, 42]
])

third_row = M[2]
second_column = M[:, 1]
element_at_2_1 = M[2, 1]
first_column_sum = np.sum(M[:, 0])
print(M.ndim)
print(M.size) # counts all elements at all levels
print(first_column_sum)

S = np.arange(9) # Array with 9 elements
S_reshaped = S.reshape(3, 3)  # Reshape into 3 rows by 3 elements
print(S_reshaped)

# COLABS
print(data.info())  # Shows data types, non-null counts
print(data.describe())  # Summary stats for numerical columns
data_loc = data.loc[data['total']>=45]
data_loc = data.iloc[7:11, :5]
data.dropna(axis=0, how='all', inplace=True) # drops all rows where values are NaN
data.drop(['index'], axis=1, inplace=True) # removes a specified column
from sklearn.impute import SimpleImputer # SimpleImputer expects a 2D array
si = SimpleImputer(strategy = 'mean') # none values replaced with the mean of the existing data (mean, median, most frequent, constant)
data.loc[:, "Exam1"] = si.fit_transform(data.loc[:, "exam1"].values.reshape(-1,1))

from google.colab import files
uploaded = files.upload()  # This opens a file dialog in Colab for you to upload files

# Mount drive in Colab
from google.colab import drive
drive.mount('/content/drive')
data = pd.read_csv('/content/drive/file.csv')
print(data.head(5)) # first 5
print(data.tail(10) # last 10
print(data[['exam1', 'exam2']] # specific columns
print(data[data['attendance'] == 0]) # specific columns with specific value
data.replace('/', np.nan, inplace=True) # replace '/' with NaN; inplace=True - update, do not create a copy of data
data.fillna(0, inplace=True) # replace Nan with zero and do not make a copy, just update
data['grade'] = pd.to_numeric(data['grade']) # convert data to numeric value
students_grade_8_plus = data[data['grade'] >= 8][['index', 'total', 'grade'] # get index, total, grade where grade >= 8
data.dropna(subset=['grade'], inplace=True) # Removes rows where the 'grade' column has NaN values.
data.reset_index(drop=True, inplace=True) # Resets the index of the DataFrame, reordering it starting from 0. drop=True prevents the old index from being added as a column.
data['Exam1_final'] = data[['exam1', 'exam1_remedial']].max(axis=1) # it takes the maxi value between the exam1 and exam1_remedial columns and stores the result in a new column called Exam1_final.
data.drop(['exam1', 'exam2', 'exam1_remedial', 'exam2_remedial'], axis=1, inplace=True) # drop columns; axis=1 - columns, not rows (0)


si = SimpleImputer(strategy = 'median')
from google.colab import files
ploaded = files.upload() # file upload prompt
data = pd.read_csv('report.csv')
resit_exam_columns = ['exam1_remedial', 'exam2_remedial']
data[resit_exam_columns] = data[resit_exam_columns].apply(pd.to_numeric, errors='coerce') # convert each column to number; errors='coerce' non-numeric values will be turned into NaN
means = data[resit_exam_columns].mean() # calculate the mean for each column
data[resit_exam_columns] = data[resit_exam_columns].fillna(means) # fill Nan with the corresponding mean value
exam_columns = ['exam1', 'exam2']
data[exam_columns] = scale(data[exam_columns]) # Scales the exam1 and exam2 columns, standardizing them (mean = 0, standard deviation = 1).
exam_columns = ['exam1_remedial', 'exam2_remedial']
minmax = MinMaxScaler()
data[exam_columns] = minmax.fit_transform(data[exam_columns].values.reshape(-2,2) # learns the scaling parameters (minimum and maximum values) from the data and rescales the data to a range between 0 and 1.
grades = data['grade'].copy() # copy column
columns=['id', 'index', 'attendance', 'exam1', 'exam2', 'exam1_remedial', 'exem2_remedial', 'total']
pd_data_array = pd.DataFrame(modified_data_array, columns) # Creates a DataFrame from the NumPy
grades_array = grades.to_numpy() # Converts the data DataFrame to a NumPy array.

