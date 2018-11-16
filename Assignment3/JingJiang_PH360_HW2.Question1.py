import hashlib

class Merkle_tree:
    def __init__(self, transactions=None):
        hashed_t = []
        for t in transactions:
            hashed_t.append(hashlib.sha256(t.encode()).hexdigest())
        self.txs = hashed_t
        self.levels = None

    def generate_tree(self):
        if len(self.txs)>0:
            self.levels = [self.txs]
            while len(self.levels[0]) > 1:
                self.generate_next_level()


    def generate_next_level(self):
        odd_node = None
        level = []
        length = len(self.levels[0])

        if length%2!=0:
            odd_node = self.levels[0][-1]
            length = len(self.levels[0])-1
        for i in range(0,length-1,2):
            j = i + 1
            lr = self.levels[0][i] + self.levels[0][j]
            level.append(hashlib.sha256(lr.encode()).hexdigest())
        if odd_node is not None:
            level.append(hashlib.sha256(odd_node.encode()).hexdigest())
        self.levels = [level] + self.levels
    
    def get_root(self):
            if self.levels is not None:
                return self.levels[0][0]
                
            else:
                return None

    def get_sibling_list(self, index):
        if self.levels is None or index > len(self.txs)-1 or index < 0:
            return None
        else:
            slist = []
            for x in range(len(self.levels)-1,0,-1):
                level_length = len(self.levels[x])
                if (index == level_length-1 and level_length%2 != 0): 
                    
                    slist.append({"left": ''})
                    index = int(index / 2)
                    
                    continue
                is_right_node = index % 2 != 0
                sibling_index = index - 1 if is_right_node else index + 1
                sibling_pos = "left" if is_right_node else "right"
                sibling_value = self.levels[x][sibling_index]
                slist.append({sibling_pos: sibling_value})
                index = int(index / 2)
            return slist

    def proof_membership(self, index, target_hash):
        merkle_root = self.get_root()
        slist = self.get_sibling_list(index)
        if len(slist) == 0:
            return target_hash == merkle_root
        else:
            proof_hash = target_hash
            for proof in slist:
                try:
                    sibling = proof['left']
                    proof_hash = hashlib.sha256((sibling + proof_hash).encode()).hexdigest()
                except:
                    sibling = proof['right']
                    proof_hash = hashlib.sha256((proof_hash + sibling).encode()).hexdigest()
            if proof_hash == merkle_root:
                return "Membership verified"
            else:
                return "Non-membership"

if __name__ == "__main__":
    m = Merkle_tree(['a', 'b', 'c', 'd', 'r'])
    m.generate_tree()
    print ('\n')

    # get root
    print ("root:", m.get_root()) 
    print ('\n')
    
    # check the membership of 'c' with its index 2
    print (m.proof_membership(2, hashlib.sha256('c'.encode()).hexdigest()))
    print ('\n')

    # check the non-membership of 'g' at an index of 1
    print (m.proof_membership(1, hashlib.sha256('g'.encode()).hexdigest()))
    print ('\n')

    # check the membership of 'r' with its index 4, showing that it works under odd number of data
    print (m.proof_membership(4, hashlib.sha256('r'.encode()).hexdigest()))
    print ('\n')