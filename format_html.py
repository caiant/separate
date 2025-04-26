def format_html_report(df):
    """Generate professional HTML report with proper styling"""
    current_time = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M %Z')
    
    
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }}
            h2 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
                margin-bottom: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 2px 3px rgba(0,0,0,0.1);
            }}
            th {{
                background-color: #3498db;
                color: white;
                text-align: center;
                padding: 12px;
                font-weight: bold;
            }}
            td {{
                padding: 10px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }}
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            tr:hover {{
                background-color: #e9f7fe;
            }}
            .positive {{
                color: #27ae60;
                font-weight: bold;
            }}
            .negative {{
                color: #e74c3c;
                font-weight: bold;
            }}
            .footer {{
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
                margin-top: 20px;
            }}
            .boe-highlight {{
                background-color: #e3f2fd;
                font-weight: bold;
                border-left: 4px solid #1976d2;
            }}
            .info-note {{
                background-color: #e8f5e9;
                padding: 8px;
                border-radius: 4px;
                margin-bottom: 15px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <h2>📈 Daily Market Report - {current_time}</h2>
        <table>
            <thead>
                <tr>
                    <th>Asset</th>
                    <th>Last Price</th>
                    <th>Change</th>
                    <th>Change %</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for _, row in df.iterrows():
        # Special formatting for BOE rate
        row_class = "boe-highlight" if "BOE Bank Rate" in row['Asset'] else ""
        
        # Color coding for changes (except BOE rate)
        change_class = ""
        if "BOE Bank Rate" not in row['Asset']:
            try:
                change_value = float(row['Change'].replace(',','').replace('%',''))
                if change_value > 0:
                    change_class = "positive"
                elif change_value < 0:
                    change_class = "negative"
            except:
                pass
        
        html += f"""
                <tr class="{row_class}">
                    <td>{row['Asset']}</td>
                    <td>{row['Last Price']}</td>
                    <td class="{change_class}">{row['Change']}</td>
                    <td class="{change_class}">{row['Change %']}</td>
                </tr>
        """
    
    html += """
            </tbody>
        </table>
        <div class="footer">
            <p>Data sources: Yahoo Finance & Bank of England | Report generated at {current_time}</p>
        </div>
    </body>
    </html>
    """
    return html
