# src/engine.py
import heapq

class RecommendationEngine:
    def __init__(self):
        # HashMap for O(1) product lookup: {product_id: Product object}
        self.catalog = {}
        # HashMap for O(1) user lookup: {user_id: User object}
        self.users = {}

    def add_product(self, product):
        self.catalog[product.product_id] = product

    def add_user(self, user):
        self.users[user.user_id] = user

    def calculate_score(self, user, product):
        """
        Calculates relevancy score: Base Rating + Category Match Weight
        """
        score = product.rating  # Base weight

        # Gather user's preferred categories based on history
        preferred_categories = set()
        for pid in user.cart.union(user.purchased).union(set(user.view_history)):
            if pid in self.catalog:
                preferred_categories.add(self.catalog[pid].category)

        # Boost score if the product matches user's preferred categories
        if product.category in preferred_categories:
            score += 3.0  # Category match weight

        return score

    def get_top_n_recommendations(self, user_id, n=3):
        """
        Uses a Priority Queue (Min-Heap) to find Top N products.
        Time Complexity: O(P log N) where P is total products.
        """
        if user_id not in self.users:
            return []

        user = self.users[user_id]
        min_heap = []

        for product_id, product in self.catalog.items():
            # Filter: Don't recommend items the user has already purchased
            if product_id in user.purchased:
                continue

            score = self.calculate_score(user, product)

            # Push to heap. Python heapq is a min-heap. 
            # We store the tuple: (score, product_id, product object)
            heapq.heappush(min_heap, (score, product.product_id, product))

            # Maintain a strict heap size of N
            if len(min_heap) > n:
                heapq.heappop(min_heap)

        # Extract items, reverse to get the highest score first
        recommendations = []
        while min_heap:
            score, pid, prod = heapq.heappop(min_heap)
            recommendations.append((prod, score))
            
        recommendations.reverse()
        return recommendations