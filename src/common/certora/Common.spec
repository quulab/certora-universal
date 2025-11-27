// Checks that all methods have a none reverting path
rule reachability(method f) {
	env e;
	calldataarg args;
	f(e,args);
	satisfy true;
}
