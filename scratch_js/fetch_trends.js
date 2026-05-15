const googleTrends = require('google-trends-api');
const fs = require('fs');

const keywordList = ['AI', 'Bitcoin', 'War', 'Inflation'];

googleTrends.interestOverTime({
  keyword: keywordList,
  startTime: new Date(Date.now() - 5 * 365 * 24 * 60 * 60 * 1000), // 5 years ago
  geo: ''
})
.then(function(results){
  const data = JSON.parse(results);
  const timelineData = data.default.timelineData;
  
  let csv = "date,AI,Bitcoin,War,Inflation\n";
  timelineData.forEach(item => {
    const dateStr = item.formattedAxisTime;
    const values = item.value.join(',');
    csv += `${dateStr},${values}\n`;
  });
  
  fs.writeFileSync('trends_data.csv', csv);
  console.log("Data saved to trends_data.csv");
})
.catch(function(err){
  console.error('Error fetching trends:', err);
});
