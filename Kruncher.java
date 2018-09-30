import java.util.Arrays;

public class Kruncher {

	
public static String[] newFridge(int n) {
	
	String [] randomIngr = {"tomato","onion", "garlic", "potato",
			"milk", "steak", "basil", "cinnamon", "clove", "white bread", 
			"salmon", "anchovy", "canned tuna", "caper", "olive", "olive oil", 
			"butter", "cream", "pickle", "shallot", "carrot", "ginger", "squash", 
			"cauliflower", "broccoli", "leek", "zucchini", "bacon", "pork tenderloin",
			"green bean", "garbanzo bean", "eggplant", "apple", "pear", "peach", 
			"cherry", "white flour", "chicken stock", "sweet potato", "red wine vinegar",
			"coriander", "mint", "fennel", "chicken breast", "pork chop", "szechuan pepper",
			"sesame oil", "avocado", "corn", "celery", "radish", "daikon", "arugula"};
	
	String [] someFridge = new String[n];
	for (int i=0; i < n; i++) {
		int index = (int)(Math.random() * randomIngr.length);
		//System.out.println(index);
		someFridge[i] = randomIngr[index];
	}
	//System.out.println(someFridge);
	return someFridge;
}

public static String[][] fridgeIterator(int m) {
	
	String [][] myFridges = new String [m][25];
	for (int i=0 ; i < m; i++) {
		//int n = (int)(Math.random() * 20);
		for (int j=0; j < 25; j++) {
			
			myFridges[i][j] = newFridge(25)[j];
		}
	}
	return myFridges;
}

public static void main(String [] args) {
	System.out.println(Arrays.toString(newFridge(25)));
	System.out.println(Arrays.deepToString(fridgeIterator(25)));
	
	}
}
