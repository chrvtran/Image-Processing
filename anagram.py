# Do not change the name of this file or the class name.

# N - number of words in Dictionary
# k - average number of letters per word

class Anagram(object):

    def __init__(self, filename):
        self.load_dictionary(filename)

    """
    Helper method to load the dictionary file.
    You may read it in some other way if you want to but do not change the function signature.
    """
    def load_dictionary(self, filename):
        with open(filename) as handle:
            self.dictionary = set(w.strip() for w in handle)
    
    """   
   * Implement the algorithm here. Do not change the function signature.
   *
   * @returns - List of lists, where each element of the outer list is a list containing all the words in that anagram class.
   * example: [['pots', 'stop', 'tops'], ['brake', 'break']]
    """
    def getAnagrams(self): # RunTime = O(N) * O(k+klgk+N) = O(N(k + klgk + N)) = O(Nk + klgk + N**2)
        result = {} # dict where {key:value} = {sorted anagram: list of anagrams}
        for word in self.dictionary: # takes O(N) for each word in dictionary
            letters = list(word) # constant time
            sortedword = "".join(self.mergeSort(letters, 0, len(letters)-1)) # join + mergeSort = O(k) + O(klgk)
            if (sortedword in result): # takes O(n) worst case (all collisions) translates to additional O(N)
                result[sortedword].append(word) # constant time
            else:
                # print(sortedword)
                result[sortedword] = [word] # constant time
                
        # for each in list(result.values()):
        #     print(each)
        return list(result.values()) # constant time
    
#     """   
#    * Converts an array of characters to a string
#    * implemented version of join()
#     """
#     def to_string(self, letters): # O(n) translates to O(k)
#         result = ""
#         for chr in letters:
#             result += chr
#         return result

    """   
   * Recursively call mergeSort on smaller segments of itself
   * @returns - list A more sorted based on ascii
    """
    def mergeSort(self, A, p, r): # we know takes O(nlgn) translates to O(klgk)
        if (p >= r):
            return A
        q = int((p+r)/2) # essentially floors
        lst = A
        lst = self.mergeSort(lst, p, q)
        lst = self.mergeSort(lst, q+1, r)
        return self.merge(lst, p, q, r) 

    """   
   * For two sorted lists within a list A, use pointers
   * to compare the ascii values for each character and swap accordingly
    """
    def merge(self, A, p, q, r): # we know takes O(n) translates to O(k)
        result = A
        L = []
        R = []
        for i in range(p, q+1):
            L.append(A[i])
        for j in range(q+1,r+1):
            R.append(A[j])
        i = 0
        j = 0
        for k in range(p, r+1):
            if i != len(L):
                if j == len(R) or ord(L[i]) <= ord(R[j]):
                    result[k] = L[i]
                    i = i + 1
                else:
                    result[k] = R[j]
                    j = j + 1
            else:
                result[k] = R[j]
                j = j + 1
        return result

"""
You can use this for debugging if you wish.
"""
if __name__ == "__main__":
    pf = Anagram("dictionary.txt")
    pf.getAnagrams()

    # pf = Anagram("dict3.txt")
    # textfile = open("anagram3.txt", "w")
    # for element in pf.getAnagrams():
    #     textfile.write(str(element) + "\n")
    # textfile.close()

