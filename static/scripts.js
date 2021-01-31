var bpm_val = 152;

function onClickIncBPM()
{
    if (bpm_val < 1000)
    {
        bpm_val += 1;
        document.getElementById("bpm_val").innerHTML = bpm_val;
    }
}

function onClickDecBPM()
{
    if (bpm_val > 0)
    {
        bpm_val -= 1;
        document.getElementById("bpm_val").innerHTML = bpm_val;
    }

}