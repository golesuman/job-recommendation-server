from collections import defaultdict
from recommendation.models import Job
from ..algorithm import TFIDF, CosineSimilarity, PearsonCorrelation
from account.models import UserProfile


class JobRecommendationServices:
    def __init__(self, documents, user_id, interaction) -> None:
        self.profile = UserProfile.objects.get(user_id=user_id)
        self.documents = documents
        self.preprocessed_documents = defaultdict()
        self.results = {}
        self.model = None
        self.cosine = CosineSimilarity()
        self.pearson = PearsonCorrelation()
        self.tfidf = TFIDF(self.preprocessed_documents)
        self.interaction = interaction
        self.preprocessed_interaction = {}
        self.preprocess()
        self.preprocess_interaction()

    def preprocess_interaction(self):
        if self.interaction:
            for document in self.interaction:
                id_ = document.job.id
                data = f"{document.job.title}"
                self.preprocessed_interaction[id_] = data

    def preprocess(self):
        for document in self.documents:
            id = document.id
            title = document.title
            description = document.description
            # job_type = document.job_type
            # location = document.location
            industry = document.industry
            category = document.category
            salary = document.skills
            data = f"{title}"

            # ]

            self.preprocessed_documents[id] = data

    def get_similarity_scores(self, n=5, model=None):
        tf_idf_matrix = self.tfidf.calculate_tfidf()

        if model == "cosine":
            for id, value in tf_idf_matrix:
                tf_idf_vector = value
                profile = self.profile
                profile_tf_idf_vector = self.tfidf.fit_document(
                    document=f"{profile.skills}"
                )
                result = self.cosine.cosine_similarity(
                    tf_idf_vector, profile_tf_idf_vector
                )
                if result > 0.4:  # please adjust values as your requirement
                    self.results[id] = result
        else:
            for id, value in tf_idf_matrix:
                tf_idf_vector = value
                for (
                    interaction_id,
                    interaction,
                ) in self.preprocessed_interaction.items():
                    job_vector = self.tfidf.fit_document(document=f"{interaction}")
                    result = self.pearson.pearson_correlation(tf_idf_vector, job_vector)
                    if result > 0.4:  # please adjust values as your requirement
                        if self.results.get(id):
                            self.results[id] += (result + self.results.get(id)) / 2
                        else:
                            self.results[id] = result

        return sorted(self.results.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_recommendations(self, n, model="cosine"):  # model is cosine by default
        scores = self.get_similarity_scores(n, model)
        return Job.objects.filter(id__in=[score[0] for score in scores])
