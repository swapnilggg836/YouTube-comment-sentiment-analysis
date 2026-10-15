import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';

const Chart = ({ data, onClick }) => {
  const labels = ['positive', 'negative', 'neutral'];

  const chartData = {
    labels,
    datasets: [{
      label: 'Comments',
      data: labels.map(label => data[label]),
      backgroundColor: ['blue', 'red', 'gray']
    }]
  };

  return (
    <>
      <h2>Sentiment Bar Chart</h2>
      <div onClick={(e) => {
        const label = labels[e.nativeEvent.target.index];
        if (label) onClick(label);
      }}>
        <Bar data={chartData} />
      </div>

      <h2>Sentiment Pie Chart</h2>
      <Pie data={chartData} />
    </>
  );
};

export default Chart;
