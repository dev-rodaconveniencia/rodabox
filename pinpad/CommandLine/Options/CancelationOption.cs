﻿using CommandLine;

namespace SimpleConsoleApp.CmdLine.Options
{
    /// <summary>
    /// Responsible for store data to cancel a transaction by it's
    /// Stone ID (Acquirer Transaction Key, ATK).
    /// </summary>
    /// <example>
    ///  cancelar  --stoneId 1234567890123 --valor 15.99
    /// </example>
    internal sealed class CancelationOption
    {
        /// <summary>
        /// Transaction ID set by Stone.
        /// </summary>
        [Option("stoneId", Required = true)]
        public string StoneId { get; set; }
        /// <summary>
        /// Transaction amount. Should match the original transaction,
        /// otherwise it will cancel the transaction partially.
        /// </summary>
        [Option("valor", Required = true)]
        public decimal Amount { get; set; }
    }
}
