from flask import Flask, render_template, request, redirect, url_for
import language_tool_python
import re

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def highlight_errors(text, matches):
    offset = 0
    for match in matches:
        start = match.offset + offset
        end = match.offset + match.errorLength + offset
        original = text[start:end]
        replacement = f'<span class="highlight-error" title="{match.message}">{original}</span>'
        text = text[:start] + replacement + text[end:]
        offset += len(replacement) - len(original)
    return text

def analyze_essay(text):
    word_count = count_words(text)
    matches = tool.check(text)
    highlighted_text = highlight_errors(text, matches)
    recommendations = [m.message for m in matches[:10]]
    grammar_issues = len(matches)
    return {
        "word_count": word_count,
        "grammar": grammar_issues,
        "recommendations": recommendations,
        "highlighted_text": highlighted_text
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    essay = request.form['comment']
    result = analyze_essay(essay)
    return render_template('results.html', **result)

@app.route('/check-again')
def check_again():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)