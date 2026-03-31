document.addEventListener('DOMContentLoaded', () => {
    const processBtn = document.getElementById('process-btn');
    const countDisplay = document.getElementById('count');
    let count = 1;

    processBtn.addEventListener('click', async () => {
        // Update count display immediately for better UX
        countDisplay.textContent = ++count;
        
        try {
            const response = await fetch(`/process?count=${count}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // Extract time portion (HH:MM:SS)
            const utcTime = data.utc_time.split(' ')[1].split('.')[0];
            const europeTime = data.europe_time.split(' ')[1].split('.')[0];
            const usEastTime = data.us_east_time.split(' ')[1].split('.')[0];
            const usWestTime = data.us_west_time.split(' ')[1].split('.')[0];
            const japanTime = data.japan_time.split(' ')[1].split('.')[0];
            const taipeiTime = data.taipei_time.split(' ')[1].split('.')[0];
            
            // Update DOM with times
            document.getElementById('utc').textContent = utcTime;
            document.getElementById('europe').textContent = europeTime;
            document.getElementById('us-east').textContent = usEastTime;
            document.getElementById('us-west').textContent = usWestTime;
            document.getElementById('japan').textContent = japanTime;
            document.getElementById('taipei').textContent = taipeiTime;
            
            // Update page title with latest time
            document.title = `Global Time Tracker - Last Update: ${utcTime}`;
        } catch (error) {
            console.error('Error fetching data:', error);
            alert('Failed to process timestamp. Please try again.');
        }
    });

    // Initial data load
    fetch('/process?count=1')
        .then(response => response.json())
        .then(data => {
            // Extract time portion for initial load
            const utcTime = data.utc_time.split(' ')[1].split('.')[0];
            const europeTime = data.europe_time.split(' ')[1].split('.')[0];
            const usEastTime = data.us_east_time.split(' ')[1].split('.')[0];
            const usWestTime = data.us_west_time.split(' ')[1].split('.')[0];
            const japanTime = data.japan_time.split(' ')[1].split('.')[0];
            const taipeiTime = data.taipei_time.split(' ')[1].split('.')[0];
            
            document.getElementById('utc').textContent = utcTime;
            document.getElementById('europe').textContent = europeTime;
            document.getElementById('us-east').textContent = usEastTime;
            document.getElementById('us-west').textContent = usWestTime;
            document.getElementById('japan').textContent = japanTime;
            document.getElementById('taipei').textContent = taipeiTime;
            
            document.title = `Global Time Tracker - Last Update: ${utcTime}`;
        })
        .catch(error => console.error('Initial load error:', error));
});
