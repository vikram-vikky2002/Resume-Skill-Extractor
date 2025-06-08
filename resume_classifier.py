import re

class ResumeClassifier:
    def __init__(self):
        self.classification_rules = {
            'Web Developer': {
                'required': ['html', 'css', 'javascript'],
                'optional': ['react', 'vue', 'angular', 'node.js', 'express', 'django', 'flask', 'rest api', 'graphql', 'typescript', 'bootstrap', 'tailwind', 'webpack', 'gulp', 'grunt', 'npm', 'yarn', 'frontend', 'web development', 'responsive design'],
                'weight': 2
            },
            'AI Engineer': {
                'required': ['python', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'numpy', 'pandas'],
                'optional': ['nlp', 'computer vision', 'opencv', 'keras', 'fastai', 'tensorflow serving', 'mlflow', 'neural networks', 'ai', 'artificial intelligence', 'data science', 'data analysis', 'neural networks', 'reinforcement learning', 'natural language processing', 'computer vision'],
                'weight': 3
            },
            'Data Scientist': {
                'required': ['python', 'r', 'data analysis', 'statistics', 'pandas', 'numpy'],
                'optional': ['sql', 'big data', 'hadoop', 'spark', 'tensorflow', 'pytorch', 'scikit-learn', 'data visualization', 'matplotlib', 'seaborn', 'tableau', 'powerbi', 'machine learning', 'data modeling', 'data wrangling', 'statistical analysis'],
                'weight': 2
            },
            'Mobile Developer': {
                'required': ['android', 'ios', 'flutter', 'react native'],
                'optional': ['swift', 'kotlin', 'java', 'xcode', 'android studio', 'mobile app', 'mobile development', 'ios development', 'android development', 'mobile ui', 'mobile ux', 'cross-platform'],
                'weight': 2
            },
            'DevOps Engineer': {
                'required': ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'git'],
                'optional': ['aws', 'azure', 'gcp', 'terraform', 'ansible', 'k8s', 'docker-compose', 'helm', 'prometheus', 'grafana', 'elk stack', 'containerization', 'automation', 'deployment', 'monitoring'],
                'weight': 2
            },
            'Cloud Engineer': {
                'required': ['aws', 'azure', 'gcp', 'cloud'],
                'optional': ['terraform', 'ansible', 'kubernetes', 'docker', 'cloud computing', 'cloud infrastructure', 'cloud services', 'cloud architecture', 'cloud security', 'cloud migration', 'cloud deployment'],
                'weight': 2
            },
            'Database Engineer': {
                'required': ['sql', 'database', 'postgresql', 'mongodb', 'mysql'],
                'optional': ['nosql', 'redis', 'cassandra', 'database design', 'database optimization', 'etl', 'data warehousing', 'big data', 'database administration', 'data modeling', 'performance tuning'],
                'weight': 2
            },
            'Backend Developer': {
                'required': ['python', 'java', 'node.js', 'ruby', 'php', 'backend', 'server-side'],
                'optional': ['django', 'flask', 'express', 'spring boot', 'ruby on rails', 'laravel', 'api development', 'restful api', 'database integration', 'server architecture', 'backend services'],
                'weight': 2
            },
            'Full Stack Developer': {
                'required': ['javascript', 'python', 'java', 'html', 'css'],
                'optional': ['react', 'node.js', 'express', 'mongodb', 'mern', 'mean', 'full-stack', 'full stack', 'full-stack development', 'frontend and backend', 'full stack development', 'web application development'],
                'weight': 3
            },
            'Cyber Security Engineer': {
                'required': ['cyber security', 'network security', 'information security', 'security protocols'],
                'optional': ['pentesting', 'vulnerability assessment', 'security analysis', 'firewall', 'ids/ips', 'encryption', 'security compliance', 'risk assessment', 'security auditing', 'security tools'],
                'weight': 2
            },
            'Network Engineer': {
                'required': ['network', 'routing', 'switching', 'network protocols'],
                'optional': ['cisco', 'juniper', 'network security', 'network design', 'network architecture', 'network troubleshooting', 'network optimization', 'wan', 'lan', 'vpn'],
                'weight': 2
            },
            'UI/UX Designer': {
                'required': ['ui design', 'ux design', 'wireframing', 'prototyping'],
                'optional': ['figma', 'sketch', 'adobe xd', 'user experience', 'user interface', 'interaction design', 'visual design', 'user research', 'user testing', 'design thinking'],
                'weight': 2
            },
            'Quality Assurance Engineer': {
                'required': ['testing', 'qa', 'quality assurance', 'test automation'],
                'optional': ['selenium', 'junit', 'pytest', 'test cases', 'test scenarios', 'test planning', 'bug tracking', 'quality control', 'test management', 'test documentation'],
                'weight': 2
            },
            'Blockchain Developer': {
                'required': ['blockchain', 'smart contracts', 'ethereum'],
                'optional': ['solidity', 'hyperledger', 'web3', 'blockchain development', 'blockchain architecture', 'cryptocurrency', 'decentralized applications', 'dapps', 'blockchain security', 'blockchain protocols'],
                'weight': 2
            },
            'Game Developer': {
                'required': ['game development', 'unity', 'unreal engine'],
                'optional': ['c#', 'c++', 'game engine', 'game design', 'game physics', 'game graphics', 'game ai', 'game programming', 'game testing', 'game optimization'],
                'weight': 2
            },
            'IoT Developer': {
                'required': ['iot', 'embedded systems', 'sensor networks'],
                'optional': ['raspberry pi', 'arduino', 'microcontroller', 'iot platform', 'iot security', 'iot architecture', 'iot protocols', 'iot devices', 'iot integration', 'iot analytics'],
                'weight': 2
            }
        }

    def classify_resume(self, skills):
        scores = {}
        
        # Convert skills to lowercase for case-insensitive matching
        skills = [skill.lower() for skill in skills]
        
        # Calculate scores for each category
        for category, rules in self.classification_rules.items():
            score = 0
            
            # Check required skills
            required_match = any(skill in skills for skill in rules['required'])
            if required_match:
                score += rules['weight'] * 2
                
            # Check optional skills
            optional_matches = sum(skill in skills for skill in rules['optional'])
            score += optional_matches * rules['weight']
            
            scores[category] = score
        
        # Find the category with the highest score
        max_score = max(scores.values())
        categories = [category for category, score in scores.items() if score == max_score]
        
        # If multiple categories have the same score, return all of them
        return categories if len(categories) > 1 else categories[0] if categories else "Uncategorized"

    def get_category_description(self, category):
        """Return a description of the category's requirements."""
        if category in self.classification_rules:
            rules = self.classification_rules[category]
            return f"Required: {', '.join(rules['required'])}\nOptional: {', '.join(rules['optional'])}"
        return ""
