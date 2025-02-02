cd /Users/saurabh/AA/convergent/Hackathons/AirOpsUpSkill/CreateFAQ/backend
poetry shell
echo "Running synthetic data generation"
python app/services/synthetic_data_generation.py
echo "Running embeddings"
python app/services/embeddings.py