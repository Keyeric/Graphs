import time
import random
import collections
class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.reset()

    def reset(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}


    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            # print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            # print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
        
        return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.reset()

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        total_friendships = num_users * avg_friendships
        added_friendships = 0
        collisions = 0
        while added_friendships < total_friendships:
            user_id_1 = random.randint(1, self.last_id)
            user_id_2 = random.randint(1, self.last_id)

            # if user_id_1 != user_id_2 and user_id_2 not in self.friendships[user_id_1]:
            if self.add_friendship(user_id_1, user_id_2):
                added_friendships += 2
            else:
                collisions += 1

        # print(f"Collisions: {collisions}")

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # visited = {}  # Note that this is a dictionary, not a set
        path_queue = collections.deque()
        # q = Queue()
        path_queue.append([user_id])
        # q.enqueue([user_id])
        while path_queue:
        # while q.size() > 0:
            path = path_queue.popleft()
            # path = q.dequeue()
            friend_id = path[-1]
            # u = path[-1]

            # if u not in visited:
                # visited[u] = path

            for id in self.friendships[friend_id]:
                # for neighbor in self.friendships[u]:
                if id not in visited:
                    new_path = path.copy()
                    # path_copy = list(path)
                    new_path.append(id)
                    path_queue.append(new_path)
                    # path_copy.append(neighbor)
                    visited[friend_id] = path

        # Figure out the number of friends / number of total users -1 to get percentage of users connected
        friend_coverage = (len(visited) - 1) / (len(self.users) - 1)
        print(f"Percentage of users that are in extended network: {friend_coverage * 100: 0.1f}%")

        # Figure average of path lengths to get average degrees of separation (subtract one to not count user)
        total_length = 0
        for path in visited.values():
            total_length += len(path) - 1

        if len(visited) > 1:
            avg_separation = total_length / (len(visited) - 1)
            print(f"Average degree of separation: {avg_separation:0.2f}")
        else:
            print("No friends")
            
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    start_time = time.time()
    sg.populate_graph(10000, 5)
    end_time = time.time()
    # print(f"Runtime: {end_time - start_time:0.2f}")
    # print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    # print(connections)
