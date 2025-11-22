# Smart Healthcare Chatbot

A Flask-based healthcare chatbot that helps users identify potential health conditions based on their symptoms through an interactive conversation flow.

## Features

- **Symptom Recognition**: Natural language processing to understand user-entered symptoms
- **Follow-up Questions**: Dynamic follow-up questions based on reported symptoms
- **Disease Diagnosis**: Matches symptoms to potential conditions from database
- **First Aid Advice**: Provides first aid suggestions and recommendations
- **Session Management**: Maintains conversation state throughout the interaction
- **Responsive UI**: Clean, mobile-friendly interface

## Project Structure

```
smart_healthcare_chatbot/
├── app/
│   ├── __init__.py
│   ├── chatbot.py          # Core conversation logic
│   ├── db.py               # Database operations
│   ├── diagnosis.py        # Diagnosis generation
│   ├── nlp.py              # Natural language processing
│   ├── routes.py           # Flask routes
│   ├── static/
│   │   └── style.css       # Styles
│   └── templates/
│       └── index.html      # Main UI
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
├── .env.example            # Environment variables template
└── README.md              # This file
```

## Database Schema

The application requires the following MySQL tables:

### 1. symptoms
```sql
CREATE TABLE symptoms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    symptom VARCHAR(255) NOT NULL,
    conditionsuggestion TEXT,
    firstaid TEXT
);
```

### 2. synonyms
```sql
CREATE TABLE synonyms (
    id INT PRIMARY KEY AUTO_INCREMENT,
    symptomid INT,
    synonymword VARCHAR(255),
    FOREIGN KEY (symptomid) REFERENCES symptoms(id)
);
```

### 3. follow_up_questions
```sql
CREATE TABLE follow_up_questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    symptomid INT,
    question_text TEXT,
    FOREIGN KEY (symptomid) REFERENCES symptoms(id)
);
```

### 4. diseases
```sql
CREATE TABLE diseases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);
```

### 5. disease_symptom
```sql
CREATE TABLE disease_symptom (
    id INT PRIMARY KEY AUTO_INCREMENT,
    diseaseid INT,
    symptomid INT,
    FOREIGN KEY (diseaseid) REFERENCES diseases(id),
    FOREIGN KEY (symptomid) REFERENCES symptoms(id)
);
```

### 6. userhistory
```sql
CREATE TABLE userhistory (
    id INT PRIMARY KEY AUTO_INCREMENT,
    userquery TEXT,
    botresponse TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd smart_healthcare_chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up MySQL database**
- Create database: `CREATE DATABASE SmartHealthChatBot;`
- Run the schema SQL statements above
- Populate tables with sample data

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Run the application**
```bash
python run.py
```

7. **Access the application**
Open browser and navigate to: `http://localhost:5000`

## Usage Flow

1. **User enters symptoms** - Type one symptom at a time (e.g., "fever", "headache")
2. **System acknowledges** - Confirms symptom is recorded
3. **User clicks "Stop"** - When finished entering all symptoms
4. **Follow-up questions** - System asks relevant follow-up questions
5. **User answers questions** - Provide answers to each question
6. **Diagnosis provided** - System shows potential condition and first aid advice
7. **Reset** - Click reset button to start new consultation

## Key Improvements Made

### 1. **Fixed NLP Matching Issue**
- Changed from token-based to substring matching
- Now properly matches multi-word symptoms
- Better handling of synonyms

### 2. **Enhanced Error Handling**
- Try-catch blocks throughout
- Graceful error messages to users
- Detailed logging for debugging

### 3. **Better Session Management**
- Proper initialization checks
- State validation
- Clear stage transitions

### 4. **Improved Database Operations**
- Connection pooling for performance
- Proper connection cleanup
- Parameterized queries (SQL injection prevention)

### 5. **Enhanced User Interface**
- Loading states
- Better visual feedback
- Responsive design
- Confirmation dialogs

### 6. **Comprehensive Logging**
- Request/response logging
- Error tracking
- Debug information

## Configuration

### Environment Variables

- `DB_HOST`: Database host (default: localhost)
- `DB_USER`: Database username (default: root)
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name (default: SmartHealthChatBot)
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_ENV`: Environment (development/production)
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)
- `PORT`: Application port (default: 5000)

## Testing

1. **Test symptom recognition**:
   - Enter "fever" - should be recognized
   - Enter "high temperature" (if synonym exists) - should match to fever

2. **Test follow-up flow**:
   - Enter multiple symptoms
   - Click Stop
   - Verify follow-up questions appear
   - Answer all questions
   - Verify diagnosis is displayed

3. **Test error handling**:
   - Enter unrecognized symptom
   - Try to stop without entering symptoms
   - Test reset functionality

## Troubleshooting

### Issue: Follow-up questions not appearing

**Solution**: Check that:
1. `follow_up_questions` table has data for your symptoms
2. `symptomid` foreign keys are correct
3. Logging shows questions are being retrieved

### Issue: Symptoms not recognized

**Solution**: Check that:
1. Symptom names in database match user input (case-insensitive)
2. Synonyms are properly linked
3. Check logs for matching attempts

### Issue: Database connection errors

**Solution**: 
1. Verify database credentials in `.env`
2. Check MySQL service is running
3. Verify database and tables exist
4. Check user has proper permissions

## License

[Your License Here]

## Contributors

[Your Name/Team]

## Support

For issues and questions, please open an issue on GitHub or contact [your-email].