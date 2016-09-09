import FileSave


class Reputation:

    def __init__(self, name="unknown", users=None):
        self.users = dict()
        if users is not None:
            self.process_users(users)
        self.name = name

    def process_users(self, users):
        for user in users:
            self.users[user['id']] = user

    def save_dictionary(self, filename):
        FileSave.save(self.users, filename)

    def restore_dictionary(self, filename):
        self.users = FileSave.load(filename)

    def process_cluster(self, cluster, is_on_topic=None):
        if is_on_topic is None:
            is_on_topic = cluster.topic == self.name
        for tweet in cluster.tweets:
            if tweet['user'] in self.users.keys():
                user = self.users[tweet['user']]
                self.process_user(user, is_on_topic)

    def update_dictionary(self, cluster, is_on_topic):
        self.process_cluster(cluster, is_on_topic)

    @staticmethod
    def process_user(user, is_on_topic):
        if 'on_topic_counter' not in user.keys():
            user['on_topic_counter'] = 0
            user['off_topic_counter'] = 0
        if is_on_topic:
            user['on_topic_counter'] += 1
        else:
            user['off_topic_counter'] += 1

    def tweet_reputation_score(self, tweet):
        if tweet['user'] in self.users.keys():
            user = self.users[tweet['user']]
            return user['on_topic_counter']
        else:
            return 0

    def reputation_score(self, cluster):
        score = 0
        for tweet in cluster:
            score += max(self.tweet_reputation_score(tweet), 3)
        return score

    def get_popular_users(self, reverse=False):
        counts_and_users = []
        for user_id in self.users.keys():
            user = self.users[user_id]
            if 'on_topic_counter' in user.keys():
                counts_and_users.append((user['on_topic_counter'], user['id']))
        counts_and_users = sorted(counts_and_users, reverse=reverse)
        users = [self.users[user_id] for (count, user_id) in counts_and_users]
        return users
