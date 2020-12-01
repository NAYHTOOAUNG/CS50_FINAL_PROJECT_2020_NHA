// Get the filter DOM element and create Onclick event which toggles the display value
var filter = document.getElementsByClassName("filter");
filter[0].addEventListener("click", function()
{
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
});

function Sort(index)
{
    // Make changes for arrow graphic in table
    var direction = ControlArrowGraphic(index);

    // Get entire rows
    var table = document.getElementById("patient");
    var rowArray = Array.from(table.getElementsByTagName("TBODY")[0].getElementsByTagName("TR"));

    // Sort entire rows and amend table
    var sorted = CombineSort(rowArray,index,direction);
    CreateSortedTable(table, sorted);
}

function EditFilter()
{
    // Get the category and query to be searched
    var searchcategory = document.getElementById("searchcategory").value;
    var query = document.getElementById("query").value;

    // Get entire rows
    var table = document.getElementById("patient");
    var rowArray = Array.from(table.getElementsByTagName("TBODY")[0].getElementsByTagName("TR"));

    // Sort the table in ascending order
    var sortedTable = CombineSort(rowArray,searchcategory,'ASC');

    // Search for the query in the previous sorted Table
    var founditem = DivideSearch(sortedTable,searchcategory,query,0,sortedTable.length);

    // If item was not found, show the whole table again
    if (!founditem) {founditem = rowArray}

    // Amend the table with found item
    CreateSearchTable(rowArray, founditem);
}

function ControlArrowGraphic(index)
{
    var direction;
    for (let i=0; i<8; i++)
    {
        // if the previous arrow is downward position and this index is clicked -> change arrow to upward position and set direction
        if (i == index && document.getElementById(`arrow${index}`).src == 'http://127.0.0.1:5000/static/red_arrow_down.svg')
        {
            document.getElementById(`arrow${index}`).src = 'static/red_arrow_up.svg';
            direction = "DESC";
        }
        // if the index matches -> change arrow to downward position and set direction
        else if (i == index )
        {
            document.getElementById(`arrow${index}`).src = 'static/red_arrow_down.svg';
            direction = "ASC";
        }

        // set the rest arrows to normal and downward positon
        else
        {
            document.getElementById(`arrow${i}`).src = 'static/arrow_down.svg';
        }
    }
    return direction;
}

function CombineSort(rows,index,direction)
{
    if (rows.length < 2)
    {
        // return item if the list contains just one item to be sorted
        return rows;
    }
    else
    {
        // take length of rows
        var rowLen = rows.length;

        // split rows into left and righ half and sort both halves
        var LeftHalf = rows.slice(0,(rowLen/2) | 0);
        var LeftSorted = CombineSort(LeftHalf,index,direction);
        var RightHalf = rows.slice((rowLen/2) | 0);
        var RightSorted = CombineSort(RightHalf,index,direction);

        // initialise sorted array
        var sorted = [];

        // do while for remaining items in one of the halves
        while (LeftSorted.length > 0 || RightSorted.length > 0)
        {
            // if left half is empty -> pust right item to sorted array
            if (LeftSorted[0] == undefined)
            {
                sorted.push(RightSorted.shift());
            }
            // if right half is empty -> push left item to sorted array
            else if (RightSorted[0] == undefined)
            {
                sorted.push(LeftSorted.shift());
            }
            else
            {
                // get the value of the searched category of the rows
                var LeftValue =  LeftSorted[0].getElementsByTagName("TD")[index].innerHTML;
                var RightValue = RightSorted[0].getElementsByTagName("TD")[index].innerHTML;

                if (compare(LeftValue,RightValue,index) <= 0)
                {
                    // if LeftValue < RightValue and direction ascending -> push left item else push right item
                    if (direction == "ASC") {sorted.push(LeftSorted.shift())}
                    else {sorted.push(RightSorted.shift())}
                }
                else
                {
                    // if RightValue < LeftValue and direction ascending -> push right item else push left item
                    if (direction == "ASC") {sorted.push(RightSorted.shift())}
                    else {sorted.push(LeftSorted.shift())}
                }
            }
        }
        return sorted;
    }
}

//Binary Search with indexes
function DivideSearch(rows,searchcategory,query,low,high)
{
    // if low bound index > upper bound index
    if (low > high)
    {
        return;
    }

    // calculate new mid index and get focus row with that index
    var mid = (low + high)/2 | 0;
    var FocusItem = rows[mid].getElementsByTagName("TD")[searchcategory].innerHTML;

    if (compare(query,FocusItem,searchcategory) == 0)
    {
        // REMOVE THE FOLLOWING LINE TO USE THE NORMAL BINARY SEARCH
        //return [rows[mid]];

        // COMMENT THE FOLLOWING 3 LINES TO USE THE NORMAL BINARY SEARCH
        // The binary search finds entire items non-stop
        var result = [rows[mid]];
        // Append the current item, the results of the LeftHalf and the results of the RightHalf
        result = result.concat(DivideSearch(rows,searchcategory,query,low,mid-1));
        result = result.concat(DivideSearch(rows,searchcategory,query,mid+1,high));

        return result;
    }
    else if (compare(query,FocusItem,searchcategory) == -1)
    {
        // if query < the current FocusItem -> set the higher bound index to lower and search in that part again
        high = mid - 1;
        return DivideSearch(rows,searchcategory,query,low,high);
    }
    else
    {
        // if query > the current FocusItem -> set the lower bound index to higher and search in that part again
        low = mid + 1;
        return DivideSearch(rows,searchcategory,query,low,high);
    }
}

// Customised compare function which can handle relevant datatypes: number, string and dates
function compare(a,b,index)
{
    if (index == 3)
    {
        // index 3 is the date column
        // convert to dates and get date time since 1.1.1980 to compare
        a = new Date(a).getTime();
        b = new Date(b).getTime();
    }
    else if (index == 0 || index == 4)
    {
        // index 0 or 4 is the integer column
        // convert each to integer
        a = parseInt(a,10);
        b = parseInt(b,10);
    }
    // return 1 when a > b, 0 when a = b, -1 when a < b
    if (a > b)
    {
        return 1;
    }
    else if (a < b)
    {
        return -1;
    }
    else
    {
        return 0;
    }

}

function CreateSortedTable(table, tableData)
{
    // create table body object
    var tableBody = document.createElement('tbody');

    // append each row of the sorted array to the tableBody DOM object
    tableData.forEach(function(row)
    {
      tableBody.appendChild(row);
    });

    // replace old tableBody with new sorted tableBody
    table.replaceChild(tableBody, table.getElementsByTagName("TBODY")[0]);
}

function CreateSearchTable(rows, tableData)
{
    // repeat each row in the table DOM Object
    rows.forEach(function(row)
    {
        // if the current focused row is in the array of elements that match the filter then show them
        if (tableData.indexOf(row) > -1) {
            row.style.display = "";
        }
        // if the current focused row is not in the array of elements that match the filter then hide them
        else
        {
            row.style.display = "none";
        }
    });
}
