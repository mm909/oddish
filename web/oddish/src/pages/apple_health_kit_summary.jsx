import React from 'react';
import ahk from '../ahk/ahk.json';
import Button1 from '../components/button/button_1';

function AppleHealthKitSummary() {
  const exportDate = new Date(ahk.metadata.export_date);
  const formattedDate = exportDate.toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short'
  });

  const quantCount = {};
  Object.keys(ahk.quantities).forEach(date => {
    const stats = ahk.quantities[date];
    Object.keys(stats).forEach(stat => {
      if (!quantCount[stat]) {
        quantCount[stat] = 0;
      }
      quantCount[stat]++;
    });
  });


  return (
    <>
      <div className='flex flex-col'>
        <div className='w-full'>
          <div className='p-4'>
            <table className='min-w-full '>
              <thead>
                <tr>
                    <td className='py-2 px-4 border-b'>Quantity</td>
                    <td className='py-2 px-4 border-b'>Days</td>
                </tr>
              </thead>
              <tbody>
                {Object.keys(quantCount).map(stat => (
                  <tr key={stat}>
                    <td className='py-2 px-4 border-b'>{stat}</td>
                    <td className='py-2 px-4 border-b'>{quantCount[stat]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className='flex flex-col items-center p-4 border-t border-black border-opacity-30'>
          <Button1 onClick={() => console.log(ahk)}>
            Console Log AHK Data
          </Button1>
          <div className='mt-2'>
            {formattedDate}
          </div>
        </div>
      </div>
  </>
  );
}

export default AppleHealthKitSummary;