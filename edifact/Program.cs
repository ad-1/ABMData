using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

/*
 * Taking an EDIFACT message text, parse out the all the LOC segments and populate
 * an array with the 2nd and 3rd element of each segment.
 * 
 * None: '+’ is an element delimiter.
 */

namespace ABMData
{
    class Program
    {

        static List<string> filteredElements = new List<string>();

        // entry point
        static void Main(string[] args)
        {
            string filepath = @"/Users/andrewdavies/PycharmProjects/ABMData/edifact/msg.txt";
            int[] indexes = { 1, 2 };
            string segId = "LOC";

            List<string> msg = ReadMsg(filepath);
            Regex pattern = new Regex("'");
            foreach (string segment in msg)
            {
                SplitSegment(segment, segId, indexes, pattern);
            }
            ShowResults();
        }

        // read edifact message
        static List<string> ReadMsg(string filepath)
        {
            List<string> msg = new List<string>();
            msg = File.ReadAllLines(filepath).ToList();
            return msg;
        }

        // split segment into elements and if 'LOC' segment get elements at specified index
        static void SplitSegment(string segment, string segId, int[] indexes, Regex pattern)
        {
            List<string> elemList = pattern.Replace(segment, "\'\\n").Split('+').ToList();
            if (elemList[0] == segId)
            {
                foreach (int i in indexes)
                {
                    if (i < elemList.Count)
                    {
                        filteredElements.Add(elemList[i]);
                    }
                }
            }
        }

        // print extracted results to console
        static void ShowResults()
        {
            foreach (string element in filteredElements)
            {
                Console.WriteLine(element);
            }
        }

    }
}
