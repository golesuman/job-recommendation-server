from collections import defaultdict
from recommendation.models import Job
from ..algorithm import CosineSimilarity
from account.models import UserProfile


class JobRecommendationServices:
    def __init__(self, documents, user_id) -> None:
        self.profile = UserProfile.objects.get(user_id=user_id)
        self.documents = documents
        self.preprocessed_documents = defaultdict()
        self.model = CosineSimilarity(self.preprocessed_documents)
        # pass

    def preprocess(self):
        for document in self.documents:
            id = document.id
            title = document.title
            description = document.description
            job_type = document.job_type
            location = document.location
            category = document.category
            salary = document.salary
            data = f"{title}, {description}, {job_type}, {location}, {category}, {salary}"
            # ]

            self.preprocessed_documents[id] = data
    def get_recommendations(self):
        profile = self.profile
        self.preprocess()
        tf_idf_matrix = self.model.calculate_tfidf()
        profile_tf_idf_vector = self.model.fit_document(
            document=f"{profile.skills},{profile.experience}, {profile.location}, {profile.preferred_industry}, {profile.bio}"
        )

        for i in range(len(tf_idf_matrix)):
            tf_idf_vector = tf_idf_matrix[i]
            
            value = self.model.cosine_similarity(tf_idf_vector,profile_tf_idf_vector)
            print(value)

        # self.model.
        # print(profile_tf_idf_vector)
        pass
