import React, { useState, useEffect } from 'react';
import { ResponsiveBar } from '@nivo/bar'
import './App.css';

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/data_daily_opp');
      const jsonData = await response.json();
      setData(jsonData);
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>My FastAPI and Vite App</h1>
        {data && (
          <div style={{ height: 400, width: '100%' }}>
            <ResponsiveBar
              data={data}
              keys={['amount']}
              indexBy="date"
              margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
              padding={0.3}
              valueScale={{ type: 'linear' }}
              indexScale={{ type: 'band', round: true }}
              colors={{ scheme: 'nivo' }}
              borderColor={{
                  from: 'color',
                  modifiers: [
                      [
                          'darker',
                          1.6
                      ]
                  ]
              }}
              axisTop={null}
              axisRight={null}
              axisBottom={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'Date',
                  legendPosition: 'middle',
                  legendOffset: 32
              }}
              axisLeft={{
                  tickSize: 5,
                  tickPadding: 5,
                  tickRotation: 0,
                  legend: 'Total opportunities (USD)',
                  legendPosition: 'middle',
                  legendOffset: -50
              }}
              labelSkipWidth={12}
              labelSkipHeight={12}
              labelTextColor={{
                  from: 'color',
                  modifiers: [
                      [
                          'darker',
                          1.6
                      ]
                  ]
              }}
              role="application"
              ariaLabel="Nivo bar chart demo"
              barAriaLabel={e=>e.id+": "+e.formattedValue+" in date: "+e.indexValue}
            />
          </div>
        )}
      </header>
    </div>
  );
};

export default App;
